# 🧱 Databricks

Anotações e notebooks sobre a plataforma Databricks, com foco em pipelines de dados e modelagem de risco de crédito.

## Tópicos

### Fundamentos (`fundamentos/`)
- Arquitetura do Databricks e Unity Catalog
- Tipos de clusters e configuração
- Databricks Asset Bundles (DAB)

### Delta Lake (`delta-lake/`)
- Formato Delta e ACID transactions
- Time travel e versionamento
- Otimização (ZORDER, OPTIMIZE, VACUUM)

### Medallion Architecture (`medallion-architecture/`)
- Camada Bronze: ingestão raw
- Camada Silver: limpeza e qualidade (DQX / Great Expectations)
- Camada Gold: agregações e feature tables

### Feature Store (`feature-store/`)
- Criação e versionamento de features
- Lookup para treinamento e inferência
- Integração com MLflow

### MLflow (`mlflow/`)
- Experiment tracking
- Model registry e ciclo de vida
- Serving e batch inference

### Spark SQL (`spark-sql/`)
- PySpark DataFrames vs SQL
- Window functions e agregações
- Performance e particionamento
