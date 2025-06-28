# Template do Projeto

O projeto está estruturado no seguinte template:

```
repos/
└── spark_projeto/
    ├── notebooks/
    │   ├── 01_exploracao_geral           # overview da base
    │   ├── 02_distribuicoes_variaveis    # histogramas, outliers
    │   ├── 03_analise_target_pd          # análise da variável default
    │   ├── 04_segmentacoes_risco         # clusterizações, scorecards
    │   └── 05_correlacoes_reducao        # correlações, PCA, VIF
    │   └── 99_utils/
    │       ├── viewer_variaveis.ipynb     # lista dicionário de variáveis
    │       └── explorador_tabelas.ipynb   # quick SQL + describe
    ├── src/
    │   ├── extract/                 # Leitura de dados (Parquet, Hive, Delta)
    │   ├── transform/               # Books de variáveis (ex: PD, LGD)
    │   ├── validate/                # Regras de qualidade, schemas
    │   ├── models/                  # Funções utilizadas para modelagem
    │   ├── load/                    # Escrita em Delta, Hive, S3
    │   └── utils/                   # Funções auxiliares (logging, parsing, etc.)
    ├── config/
    │   └── paths.py                       # nomes padrão de tabelas do catálogo
    ├── tests/
    │   └── test_transform.py              # testes de features
    ├── jobs/
        └── run_pipeline.py              # Orquestra o pipeline completo
    ├── requirements.txt
    └── README.md
```