# Dicionário de Dados

## Dataset original

| Campo | Descrição | Tipo | Uso |
|---|---|---:|---|
| `tau1` | Tempo de reação do produtor de energia | Numérico | Feature |
| `tau2` | Tempo de reação do consumidor 1 | Numérico | Feature |
| `tau3` | Tempo de reação do consumidor 2 | Numérico | Feature |
| `tau4` | Tempo de reação do consumidor 3 | Numérico | Feature |
| `p1` | Potência nominal produzida pelo nó produtor | Numérico | Feature |
| `p2` | Potência nominal consumida pelo consumidor 1 | Numérico | Feature |
| `p3` | Potência nominal consumida pelo consumidor 2 | Numérico | Feature |
| `p4` | Potência nominal consumida pelo consumidor 3 | Numérico | Feature |
| `g1` | Elasticidade/preço do produtor | Numérico | Feature |
| `g2` | Elasticidade/preço do consumidor 1 | Numérico | Feature |
| `g3` | Elasticidade/preço do consumidor 2 | Numérico | Feature |
| `g4` | Elasticidade/preço do consumidor 3 | Numérico | Feature |
| `stab` | Medida contínua de estabilidade | Numérico | Target de regressão |
| `stabf` | Classe de estabilidade (`stable`/`unstable`) | Categórico | Target de classificação |

## Variáveis derivadas

| Campo | Descrição |
|---|---|
| `tempo_resposta_medio` | Média dos tempos `tau1` a `tau4` |
| `tempo_resposta_max` | Maior tempo de reação entre os quatro nós |
| `potencia_total_consumo` | Soma absoluta das potências consumidoras `p2`, `p3`, `p4` |
| `potencia_produtor` | Potência produzida pelo nó central `p1` |
| `elasticidade_media` | Média das elasticidades `g1` a `g4` |
| `elasticidade_max` | Maior elasticidade entre os quatro nós |
| `is_unstable` | 1 para instável e 0 para estável |
| `grid_risk_score` | Índice sintético para ranking de risco operacional |
