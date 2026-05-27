# Pitch Final — 5 minutos

## 1. O problema complexo — 1 min

Smart Grids são redes elétricas inteligentes que usam sensores, comunicação e controle descentralizado para equilibrar produção e consumo de energia. O problema é que pequenas variações de tempo de resposta, consumo e elasticidade podem causar instabilidade no sistema. Se a rede só reage depois da falha, o impacto operacional e financeiro já aconteceu.

## 2. A Engenharia de Dados — 1 min

O grupo construiu um pipeline ETL em Python no Google Colab. Os dados são extraídos de fonte externa pública, persistidos em camada raw, tratados na camada silver e reorganizados em Star Schema na camada gold. A modelagem dimensional separa perfis de potência, tempo de resposta, elasticidade e classe de estabilidade.

## 3. A Inteligência — 1 min

Foram treinados modelos de Machine Learning para prever se a rede está estável ou instável. O notebook compara modelos lineares e baseados em árvore usando métricas como acurácia, precision, recall, F1-Score e ROC-AUC. O modelo campeão é escolhido pela melhor capacidade de detectar instabilidade.

## 4. O Dashboard de Decisão — 1 min

A camada de BI apresenta indicadores como percentual de cenários instáveis, distribuição das variáveis críticas, matriz de correlação e simulação OLAP por faixas de tempo de resposta e elasticidade. Isso transforma o resultado técnico em informação clara para tomada de decisão.

## 5. O impacto — 1 min

O projeto mostra como IA pode apoiar a prevenção de falhas em redes elétricas inteligentes. O impacto está em reduzir indisponibilidade, priorizar manutenção, melhorar confiabilidade e apoiar decisões estratégicas em energia renovável e infraestrutura crítica.
