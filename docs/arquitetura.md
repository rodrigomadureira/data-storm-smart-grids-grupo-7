# Arquitetura do Projeto — Star Schema

## Visão geral

O projeto utiliza uma arquitetura analítica simples, porém completa:

1. **Camada Raw/Bronze:** dataset original baixado da UCI.
2. **Camada Silver:** limpeza, padronização, tipagem e criação de variáveis derivadas.
3. **Camada Gold:** modelagem dimensional em Star Schema.
4. **Camada Analytics:** EDA, Machine Learning e Business Insights.

## Star Schema

```mermaid
erDiagram
    DIM_SIMULATION ||--o{ FACT_GRID_STABILITY : simulation_id
    DIM_POWER_PROFILE ||--o{ FACT_GRID_STABILITY : power_profile_id
    DIM_RESPONSE_PROFILE ||--o{ FACT_GRID_STABILITY : response_profile_id
    DIM_ELASTICITY_PROFILE ||--o{ FACT_GRID_STABILITY : elasticity_profile_id
    DIM_STABILITY_CLASS ||--o{ FACT_GRID_STABILITY : stability_class_id

    DIM_SIMULATION {
        int simulation_id PK
        string source_dataset
        string source_url
        datetime extraction_timestamp
    }

    DIM_POWER_PROFILE {
        int power_profile_id PK
        float p1
        float p2
        float p3
        float p4
        float total_consumption
        float producer_power
    }

    DIM_RESPONSE_PROFILE {
        int response_profile_id PK
        float tau1
        float tau2
        float tau3
        float tau4
        float avg_response_time
        float max_response_time
    }

    DIM_ELASTICITY_PROFILE {
        int elasticity_profile_id PK
        float g1
        float g2
        float g3
        float g4
        float avg_elasticity
        float max_elasticity
    }

    DIM_STABILITY_CLASS {
        int stability_class_id PK
        string stability_label
        int is_unstable
        string risk_level
    }

    FACT_GRID_STABILITY {
        int fact_id PK
        int simulation_id FK
        int power_profile_id FK
        int response_profile_id FK
        int elasticity_profile_id FK
        int stability_class_id FK
        float stab_value
        float grid_risk_score
    }
```

## Justificativa técnica

A modelagem separa características operacionais em dimensões analíticas. Isso facilita consultas OLAP, segmentações por perfil de potência, resposta e elasticidade, além de permitir análise histórica caso novos lotes de dados sejam incorporados ao pipeline.
