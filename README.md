# 🧠 Repositório de Anotações em Ciência de Dados

Este repositório reúne minhas anotações pessoais, resumos técnicos e aprendizados práticos ao longo da minha jornada como Cientista de Dados.

O objetivo é consolidar, revisar e compartilhar conhecimentos de forma organizada, cobrindo temas essenciais da área — desde fundamentos estatísticos até aplicações avançadas em machine learning, engenharia de dados e regulamentações aplicadas ao setor financeiro (como IFRS 9 e Resolução 4.966 do BACEN).

---

### 🔖 Tipos de commit (padronização)

| Tag        | Descrição                                             |
|------------|--------------------------------------------------------|
| `docs`     | Alteração de documentação                              |
| `experiment` | Testes exploratórios                                 |
| `feature`  | Nova funcionalidade                                    |
| `fix`      | Correção de erro                                       |
| `model`    | Treinamento ou tuning de modelo                        |
| `perf`     | Mudança de código focada em melhorar performance       |
| `refactor` | Refatoração de código existente (sem mudar funcionalidade) |

---

# 📘 Trilha de Estudos: Machine Learning para Risco de Crédito (com base no ESL)

> Baseado no livro _The Elements of Statistical Learning_ com aplicações em inadimplência, scorecards e IFRS 9.

---

## 🧱 Módulo 1 – Fundamentos Estatísticos e Pré-processamento

- [ ] Reforçar conceitos de probabilidade e inferência com Casella & Berger
- [ ] Realizar análise exploratória (EDA) em bases como HMEQ
- [ ] Identificar e tratar outliers e valores ausentes
- [ ] Aplicar técnicas de normalização, binning supervisionado e WOE

---

## 🌲 Módulo 2 – Métodos Lineares para Classificação

- [ ] Estudar Regressão Logística (Cap. 4 do ESL)
- [ ] Explorar regularização Lasso e Ridge (Cap. 3)
- [ ] Aplicar Análise Discriminante Linear (LDA)
- [ ] Implementar um scorecard com `scorecardpy` ou `statsmodels`

---

## 🌳 Módulo 3 – Métodos Não Lineares e Árvores

- [ ] Entender árvores de decisão e suas divisões (Cap. 9)
- [ ] Aplicar Random Forest e Bagging (Cap. 15)
- [ ] Implementar modelos com Boosting (Cap. 10) usando LightGBM
- [ ] Comparar performance entre Logit e Gradient Boosting com HMEQ

---

## ⛓ Módulo 4 – Modelos de Tempo e Sobrevivência

- [ ] Estudar Hazard Models (discreto e contínuo)
- [ ] Aplicar o modelo de Cox com `lifelines`
- [ ] Trabalhar com covariáveis dependentes do tempo
- [ ] Implementar modelagem de PD com sobrevivência (ex: `pycox`)

---

## 🧪 Módulo 5 – Validação, Performance e Dados Desbalanceados

- [ ] Avaliar modelos com AUC, KS, Lift, Precision/Recall
- [ ] Tratar dados desbalanceados com SMOTE e undersampling
- [ ] Calcular e monitorar o PSI para estabilidade de variáveis
- [ ] Implementar validação cruzada e holdout temporal

---

## 🧠 Módulo 6 – Modelos Avançados e Interpretação

- [ ] Explorar SVM e Kernel Methods (Cap. 12)
- [ ] Estudar técnicas de explicabilidade (SHAP, LIME)
- [ ] Trabalhar com modelos de múltiplas saídas (Cap. 11)
- [ ] Estimar PD, LGD e EAD em tarefas multi-target

---

## 📦 Recursos Complementares

- [ ] Baixar bases públicas: HMEQ, Lending Club, Home Credit (Kaggle)
- [ ] Estudar IFRS 9, Resolução CMN 4966 e Basel II/III
- [ ] Familiarizar-se com `scikit-learn`, `lightgbm`, `lifelines`, `statsmodels`
- [ ] Revisar capítulos específicos no livro _Credit Risk Analytics_ (Baesens)

---

# ⚡ Trilha de Estudos PySpark

Checklist com os principais tópicos que um cientista de dados deve dominar para trabalhar com PySpark em ambientes de big data, incluindo transformações, modelagem e performance.

## ✅ Fundamentos do PySpark
- [ ] O que é PySpark e como ele se integra com Apache Spark  
- [ ] Instalação e primeiros passos (SparkSession, SparkContext)  
- [ ] Diferenças entre RDD, DataFrame e Dataset  
- [ ] Leitura e escrita de arquivos (CSV, JSON, Parquet)  
- [ ] Schema explícito vs. inferência automática  
- [ ] Trabalhando com `show()`, `printSchema()`, `describe()`, `select()`  

## 🧪 Manipulação de Dados com DataFrames
- [ ] Filtros (`filter()`, `where()`)  
- [ ] Seleção e renomeação de colunas  
- [ ] Criação de colunas com `withColumn()` e `expr()`  
- [ ] Funções nativas (`when`, `col`, `lit`, `isNull`, `isin`)  
- [ ] Joins (`inner`, `left`, `right`, `outer`, `semi`, `anti`)  
- [ ] Agrupamentos e agregações com `groupBy()`  
- [ ] Window functions (`row_number`, `rank`, `lag`, `lead`)  
- [ ] Tratamento de valores nulos e duplicados  

## 🔄 Transformações Avançadas e Performance
- [ ] Lazy evaluation: como funciona e por que importa  
- [ ] Particionamento e `repartition()` vs. `coalesce()`  
- [ ] Broadcast joins e quando utilizá-los  
- [ ] Caching com `cache()` e `persist()`  
- [ ] UDFs e Pandas UDFs (User Defined Functions)  
- [ ] Leitura eficiente com `.option()`, `.schema()`, `.mode()`  

## 🧱 Estrutura de Projetos com PySpark
- [ ] Organização de scripts em pipelines  
- [ ] Modularização de jobs com funções e classes  
- [ ] Parâmetros via `argparse` ou arquivos `.yaml/.json`  
- [ ] Integração com Git e versionamento de código Spark  

## 🔁 PySpark SQL
- [ ] Uso de SQL diretamente com `spark.sql()`  
- [ ] Registro de views temporárias e permanentes  
- [ ] Conversão entre SQL e API DataFrame  

## 📈 Machine Learning com MLlib
- [ ] Conceito de pipelines (`Pipeline`, `PipelineModel`)  
- [ ] Estimators e Transformers  
- [ ] Feature engineering com `VectorAssembler`, `StringIndexer`, `OneHotEncoder`  
- [ ] Treinamento de modelos (`LogisticRegression`, `RandomForest`, etc.)  
- [ ] Avaliação com `BinaryClassificationEvaluator`, `RegressionEvaluator`  
- [ ] Cross-validation com `ParamGridBuilder` e `CrossValidator`  

## 🌐 Integração com o ecossistema
- [ ] Integração com Hive e Catálogo externo  
- [ ] Conexão com bancos de dados via JDBC  
- [ ] Escrita em Delta Lake (se aplicável)  
- [ ] Execução no Databricks ou EMR  
- [ ] Integração com ferramentas de orquestração (Airflow, dbutils, etc.)

## 📚 Extras e Boas Práticas
- [ ] Logging com `log4j` e controle de erros  
- [ ] Testes unitários com `pytest` em código PySpark  
- [ ] Uso de `config` e tuning com `spark.conf.set()`  
- [ ] Gerenciamento de recursos: executores, memória, partições  
- [ ] Debugging em cluster (logs e UI do Spark)  
- [ ] Análise de DAGs no Spark UI  

---

# 🧠 Trilha de Programação Orientada a Objetos

Uma lista com os principais tópicos de POO que um cientista de dados deve dominar para estruturar códigos mais robustos, reutilizáveis e escaláveis com Python.

## ✅ Fundamentos da Programação Orientada a Objetos
- [ ] O que é POO? Paradigmas imperativos vs. orientados a objetos  
- [ ] Conceitos de Classe e Objeto  
- [ ] Atributos de instância vs. atributos de classe  
- [ ] Métodos de instância  
- [ ] Construtor (`__init__`) e inicialização de objetos  
- [ ] Representação com `__str__()` e `__repr__()`  
- [ ] Atributos privados (`_`, `__`) e convenções

## 🔁 Encapsulamento e Propriedades
- [ ] Encapsulamento: o que é e por que importa  
- [ ] Getters e setters em Python  
- [ ] Uso do decorador `@property`  
- [ ] Controle de acesso (simulado) com underscores

## 🧬 Herança e Composição
- [ ] Herança simples e múltipla  
- [ ] `super()` e chamada da superclasse  
- [ ] Override de métodos  
- [ ] `isinstance()` e `issubclass()`  
- [ ] Composição vs. herança (preferência por composição)

## 🧩 Polimorfismo
- [ ] Métodos com o mesmo nome em classes diferentes  
- [ ] Duck typing: “if it quacks like a duck…”  
- [ ] Uso prático em código genérico e testes

## 🧱 Classes Abstratas e Interfaces
- [ ] Módulo `abc` e classe `ABC`  
- [ ] Métodos abstratos com `@abstractmethod`  
- [ ] Por que usar classes abstratas em pipelines de ML ou ETL?

## 📦 Organização e Design
- [ ] Módulos e pacotes em Python  
- [ ] Organização de múltiplas classes em um projeto  
- [ ] Inversão de dependência básica  
- [ ] SOLID principles (resumidamente)

## 🧪 Aplicações Práticas em Ciência de Dados
- [ ] Criar uma classe `Dataset` que encapsula limpeza, validação e transformação  
- [ ] Criar uma classe `FeatureEngineer` com métodos como `.scale()`, `.encode()`  
- [ ] Classe `ModelWrapper` para encapsular modelo, predict e métricas  
- [ ] Abstração para múltiplos modelos (`Regressor`, `Classifier`, etc.)  
- [ ] Implementação de pipelines com objetos customizados  
- [ ] Projeto final: mini framework com suas próprias classes de modelagem

## 🧠 Extras (bons diferenciais)
- [ ] Uso de `__slots__` para otimização de memória  
- [ ] Métodos mágicos (`__eq__`, `__len__`, `__iter__`, etc.)  
- [ ] Introdução a design patterns (Factory, Strategy, etc.)  
- [ ] Decoradores de classe e `@classmethod`, `@staticmethod`  
- [ ] Testes com classes: usando `pytest` e `unittest`
