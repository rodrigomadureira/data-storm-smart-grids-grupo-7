"""Pipeline de dados do projeto DATA_STORM — Grupo 7 — Smart Grids."""
from __future__ import annotations

from pathlib import Path
from datetime import datetime
import io
import zipfile
import requests
import numpy as np
import pandas as pd

UCI_ZIP_URL = "https://archive.ics.uci.edu/static/public/471/electrical+grid+stability+simulated+data.zip"
GITHUB_RAW_URL = "https://raw.githubusercontent.com/rahatUlAin/Electrical-Grid-Stability-Simulated-Data-/master/Data_for_UCI_named.csv"


def load_dataset() -> pd.DataFrame:
    """Carrega o dataset de Smart Grid da UCI com fallback em CSV público."""
    try:
        response = requests.get(UCI_ZIP_URL, timeout=30)
        response.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
            csv_files = [name for name in zf.namelist() if name.lower().endswith(".csv")]
            if not csv_files:
                raise FileNotFoundError("Nenhum CSV encontrado no ZIP da UCI.")
            with zf.open(csv_files[0]) as file:
                return pd.read_csv(file)
    except Exception:
        return pd.read_csv(GITHUB_RAW_URL)


def transform_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Limpa, padroniza e cria variáveis derivadas."""
    df = df.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]
    df = df.drop_duplicates().dropna()

    numeric_cols = [c for c in df.columns if c != "stabf"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna()

    tau_cols = ["tau1", "tau2", "tau3", "tau4"]
    p_cols = ["p1", "p2", "p3", "p4"]
    g_cols = ["g1", "g2", "g3", "g4"]

    df["tempo_resposta_medio"] = df[tau_cols].mean(axis=1)
    df["tempo_resposta_max"] = df[tau_cols].max(axis=1)
    df["potencia_total_consumo"] = df[["p2", "p3", "p4"]].abs().sum(axis=1)
    df["potencia_produtor"] = df["p1"]
    df["elasticidade_media"] = df[g_cols].mean(axis=1)
    df["elasticidade_max"] = df[g_cols].max(axis=1)
    df["is_unstable"] = df["stabf"].str.lower().eq("unstable").astype(int)
    df["grid_risk_score"] = (
        df["tempo_resposta_medio"].rank(pct=True) * 0.35
        + df["tempo_resposta_max"].rank(pct=True) * 0.25
        + df["potencia_total_consumo"].rank(pct=True) * 0.20
        + df["elasticidade_media"].rank(pct=True) * 0.20
    )
    df.insert(0, "simulation_id", np.arange(1, len(df) + 1))
    return df


def build_star_schema(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Cria dimensões e fato em Star Schema."""
    df = df.copy()

    dim_simulation = pd.DataFrame({
        "simulation_id": df["simulation_id"],
        "source_dataset": "UCI Electrical Grid Stability Simulated Data",
        "source_url": UCI_ZIP_URL,
        "extraction_timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    })

    def build_dim(source: pd.DataFrame, cols: list[str], key: str) -> pd.DataFrame:
        dim = source[cols].drop_duplicates().reset_index(drop=True)
        dim.insert(0, key, np.arange(1, len(dim) + 1))
        return dim

    dim_power = build_dim(
        df,
        ["p1", "p2", "p3", "p4", "potencia_total_consumo", "potencia_produtor"],
        "power_profile_id",
    )
    dim_response = build_dim(
        df,
        ["tau1", "tau2", "tau3", "tau4", "tempo_resposta_medio", "tempo_resposta_max"],
        "response_profile_id",
    )
    dim_elasticity = build_dim(
        df,
        ["g1", "g2", "g3", "g4", "elasticidade_media", "elasticidade_max"],
        "elasticity_profile_id",
    )
    dim_stability = pd.DataFrame({
        "stability_class_id": [1, 2],
        "stability_label": ["stable", "unstable"],
        "is_unstable": [0, 1],
        "risk_level": ["Operação normal", "Risco operacional"],
    })

    fact = df.merge(dim_power, on=["p1", "p2", "p3", "p4", "potencia_total_consumo", "potencia_produtor"], how="left")
    fact = fact.merge(dim_response, on=["tau1", "tau2", "tau3", "tau4", "tempo_resposta_medio", "tempo_resposta_max"], how="left")
    fact = fact.merge(dim_elasticity, on=["g1", "g2", "g3", "g4", "elasticidade_media", "elasticidade_max"], how="left")
    fact = fact.merge(dim_stability[["stability_class_id", "stability_label"]], left_on="stabf", right_on="stability_label", how="left")

    fact = fact[[
        "simulation_id", "power_profile_id", "response_profile_id", "elasticity_profile_id",
        "stability_class_id", "stab", "grid_risk_score"
    ]].copy()
    fact.insert(0, "fact_id", np.arange(1, len(fact) + 1))
    fact = fact.rename(columns={"stab": "stab_value"})

    return {
        "dim_simulation": dim_simulation,
        "dim_power_profile": dim_power,
        "dim_response_profile": dim_response,
        "dim_elasticity_profile": dim_elasticity,
        "dim_stability_class": dim_stability,
        "fact_grid_stability": fact,
    }


def save_tables(tables: dict[str, pd.DataFrame], output_dir: str | Path) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, table in tables.items():
        table.to_csv(output_dir / f"{name}.csv", index=False)
