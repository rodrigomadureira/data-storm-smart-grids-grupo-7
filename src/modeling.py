"""Modelagem preditiva do projeto DATA_STORM — Grupo 7 — Smart Grids."""
from __future__ import annotations

import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

FEATURES = [
    "tau1", "tau2", "tau3", "tau4",
    "p1", "p2", "p3", "p4",
    "g1", "g2", "g3", "g4",
    "tempo_resposta_medio", "tempo_resposta_max",
    "potencia_total_consumo", "potencia_produtor",
    "elasticidade_media", "elasticidade_max",
    "grid_risk_score",
]


def train_classifiers(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    X = df[FEATURES]
    y = df["is_unstable"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    models = {
        "Logistic Regression": Pipeline([
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(max_iter=2000, class_weight="balanced")),
        ]),
        "Decision Tree": DecisionTreeClassifier(max_depth=8, random_state=42, class_weight="balanced"),
        "Random Forest": RandomForestClassifier(n_estimators=250, max_depth=None, random_state=42, class_weight="balanced", n_jobs=-1),
        "Neural Network (MLP)": Pipeline([
            ("scaler", StandardScaler()),
            ("model", MLPClassifier(hidden_layer_sizes=(32, 16), max_iter=500, random_state=42)),
        ]),
    }

    results = []
    fitted = {}
    for name, model in models.items():
        start = time.perf_counter()
        model.fit(X_train, y_train)
        elapsed = time.perf_counter() - start
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else y_pred
        results.append({
            "modelo": name,
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall": recall_score(y_test, y_pred, zero_division=0),
            "f1": f1_score(y_test, y_pred, zero_division=0),
            "roc_auc": roc_auc_score(y_test, y_prob),
            "tempo_execucao_s": elapsed,
        })
        fitted[name] = model

    return pd.DataFrame(results).sort_values("f1", ascending=False), fitted
