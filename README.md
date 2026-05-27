# DATA_STORM — Grupo 7 — Smart Grids

Projeto final da disciplina **Análise de Dados (ANALDA-101002)**.

## Tema

**Soberania de Dados e IA em Redes de Energia Inteligentes (Smart Grids)**  
Previsão de estabilidade operacional em redes elétricas inteligentes utilizando Engenharia de Dados, EDA, Modelagem Preditiva e Business Insights.

## Integrantes

- Estela Argolo
- William Henrique
- Rodrigo Madureira

## Problema de negócio

Redes elétricas inteligentes dependem de sensores, resposta dinâmica de consumidores/produtores e mecanismos de controle descentralizado. Pequenas variações no tempo de resposta, potência e elasticidade de preço podem tornar a rede instável.

O projeto propõe um pipeline analítico para responder:

> **É possível prever automaticamente se uma Smart Grid está estável ou instável, permitindo ações preventivas antes de falhas operacionais?**

## Dataset

Fonte principal: **UCI Machine Learning Repository — Electrical Grid Stability Simulated Data**.

O dataset possui simulações de uma rede elétrica de 4 nós, com variáveis de tempo de reação, potência nominal e elasticidade/preço. Ele permite tarefas de **classificação** (`stable`/`unstable`) e **regressão** (`stab`).

## Estrutura do repositório

```text
data-storm-smart-grids-grupo-7/
├── notebooks/
│   └── DATA_STORM_GRUPO_7_SMART_GRIDS.ipynb
├── src/
│   ├── data_pipeline.py
│   └── modeling.py
├── docs/
│   ├── arquitetura.md
│   ├── dicionario_dados.md
│   └── pitch_5min.md
├── data/
│   ├── raw/.gitkeep
│   └── processed/.gitkeep
├── outputs/
│   ├── figures/.gitkeep
│   └── models/.gitkeep
├── requirements.txt
├── .gitignore
└── README.md
```

## Entregáveis atendidos

- Arquitetura de Data Warehouse em **Star Schema**.
- Pipeline ETL funcional no Google Colab.
- Persistência dos dados brutos e tratados em estrutura `/data/raw` e `/data/processed`.
- EDA com estatística descritiva, dispersão, assimetria, curtose, outliers e correlação.
- Comparativo entre múltiplos modelos de ML.
- Métricas: Acurácia, Precision, Recall, F1-Score, ROC-AUC e RMSE.
- Simulação OLAP/BI com tabelas dinâmicas e recomendações estratégicas.
- Pitch final de 5 minutos documentado.

## Como executar

### No Google Colab

1. Abra o notebook `notebooks/DATA_STORM_GRUPO_7_SMART_GRIDS.ipynb`.
2. Execute as células em ordem.
3. Ao executar no Colab, os dados serão persistidos automaticamente no Google Drive, se o Drive for montado.
4. Ao final, o notebook gera:
   - tabelas raw/processed;
   - dimensões e fato;
   - gráficos de EDA;
   - métricas dos modelos;
   - recomendações executivas.

### Localmente

```bash
pip install -r requirements.txt
jupyter notebook notebooks/DATA_STORM_GRUPO_7_SMART_GRIDS.ipynb
```

## Modelo campeão esperado

O notebook compara modelos lineares e não lineares. Em geral, modelos baseados em árvore, especialmente **Random Forest**, tendem a capturar melhor relações não lineares entre tempo de resposta, potência e elasticidade.

## Conclusão executiva

A solução permite classificar cenários de operação da rede como **estáveis** ou **instáveis**, apoiando ações preventivas como ajuste de controle, priorização de nós críticos, revisão de políticas de resposta à demanda e monitoramento proativo.
