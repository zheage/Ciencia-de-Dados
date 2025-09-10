# 🧠 Repositório de Anotações em Ciência de Dados

Este repositório reúne minhas anotações pessoais, resumos técnicos e aprendizados práticos ao longo da minha jornada como Cientista de Dados.

O objetivo é consolidar, revisar e compartilhar conhecimentos de forma organizada, cobrindo temas essenciais da área — desde fundamentos estatísticos até aplicações avançadas em machine learning, engenharia de dados e regulamentações aplicadas ao setor financeiro (como IFRS 9 e Resolução 4.966 do BACEN).

---

### 🔖 Tipos de commit (padronização)

| Tag        | Descrição                                              |
|------------|--------------------------------------------------------|
| `docs`     | Alteração de documentação                              |
| `experiment` | Testes exploratórios                                 |
| `feature`  | Nova funcionalidade                                    |
| `fix`      | Correção de erro                                       |
| `model`    | Treinamento ou tuning de modelo                        |
| `perf`     | Mudança de código focada em melhorar performance       |
| `refactor` | Refatoração de código existente (sem mudar funcionalidade) |

---

# ⚡ Trilha de Estudos PySpark

Checklist com os principais tópicos que um cientista de dados deve dominar para trabalhar com PySpark em ambientes de big data, incluindo transformações, modelagem e performance.

## ✅ Fundamentos do PySpark
- [ ] O que é PySpark e como ele se integra com Apache Spark  
- [ ] Instalação e primeiros passos (SparkSession, SparkContext)  
- [ ] Diferenças entre RDD, DataFrame e Dataset  
- [ ] Leitura e escrita de arquivos (CSV, JSON, Parquet)  
- [ ] Schema explícito vs. inferência automática  
- [x] Trabalhando com `show()`, `printSchema()`, `describe()`, `select()`  
- [ ] Trabalhando com `show()`, `printSchema()`, `describe()`, `select()`  n

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
- [x] Particionamento e `repartition()` vs. `coalesce()`  
- [x] Particionamento: `repartition()` vs. `coalesce()`  
- [x] Broadcast joins e quando utilizá-los  
- [x] Caching com `cache()` e `persist()`  
- [ ] UDFs e Pandas UDFs (User Defined Functions)  
- [ ] Leitura eficiente com `.option()`, `.schema()`, `.mode()`  

## 🧱 Estrutura de Projetos com PySpark
- [x] Organização de scripts em pipelines  
- [ ] Modularização de jobs com funções e classes  
- [ ] Parâmetros via `argparse` ou arquivos `.yaml/.json`  
- [ ] Integração com Git e versionamento de código Spark  

## 🔁 PySpark SQL
- [x] Uso de SQL diretamente com `spark.sql()`  
- [x] Registro de views temporárias e permanentes  
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

## ✅ Roadmap SQL


## 📘 Fundamentos de SQL
- [x] **SELECT, FROM, WHERE** – Sintaxe básica para consultar dados de uma tabela.
- [ ] **Operadores (IN, LIKE, BETWEEN, IS NULL)** – Filtros comuns para valores, padrões e faixas.
- [x] **ORDER BY, LIMIT** – Ordenação de resultados e limitação de registros retornados.
- [x] **Aliases (`AS`)** – Dar nomes alternativos a colunas ou tabelas para facilitar a leitura.

## 🧮 Agregações e Agrupamentos
- [x] **COUNT, SUM, AVG, MIN, MAX** – Funções agregadoras para sumarizar dados.
- [x] **GROUP BY** – Agrupar registros por uma ou mais colunas.
- [ ] **HAVING** – Filtrar resultados após o `GROUP BY`.
- [x] **DISTINCT** – Remover duplicatas nos resultados.

## 🔗 Joins (Junções entre tabelas)
- [x] **INNER JOIN** – Retorna registros com correspondência nas duas tabelas.
- [x] **LEFT JOIN / RIGHT JOIN** – Inclui todos os registros da tabela da esquerda/direita.
- [ ] **FULL OUTER JOIN** – Inclui todos os registros de ambas as tabelas, com ou sem correspondência.
- [ ] **CROSS JOIN** – Produto cartesiano entre duas tabelas.
- [ ] **SELF JOIN** – Tabela unida com ela mesma para relações hierárquicas ou comparações.

## 🧱 Subqueries e CTEs
- [ ] **Subqueries em SELECT, FROM, WHERE** – Consultas aninhadas para filtragem ou cálculo.
- [ ] **CTE com `WITH`** – Nomear subqueries reutilizáveis, melhorando legibilidade.
- [ ] **CTE Recursiva** – Para hierarquias (ex: organogramas, categorias encadeadas).

## 🪟 Window Functions (Funções de Janela)
- [ ] **ROW_NUMBER, RANK, DENSE_RANK** – Ordenar e numerar registros dentro de partições.
- [ ] **LAG, LEAD** – Acessar valores anteriores ou posteriores sem auto-joins.
- [ ] **FIRST_VALUE, LAST_VALUE** – Retornar o primeiro ou último valor da partição.
- [ ] **OVER (PARTITION BY ... ORDER BY ...)** – Definir o escopo e ordem das janelas.

## 🧹 Manipulação e Limpeza de Dados
- [ ] **CASE WHEN** – Expressões condicionais tipo `if/else` para criar colunas derivadas.
- [ ] **COALESCE, NULLIF** – Substituição e comparação com valores nulos.
- [ ] **CAST, CONVERT** – Conversão entre tipos (string, inteiro, data etc.).
- [ ] **TRIM, SUBSTRING, UPPER, LOWER** – Funções de texto e limpeza de strings.

## 🗂️ Modelagem e Performance
- [ ] **Normalização e Desnormalização** – Estruturar dados para consistência e/ou performance.
- [ ] **CREATE TABLE, tipos de dados** – Definir esquemas e estruturas de tabelas.
- [ ] **Índices e Chaves** – Melhorar performance de busca e integridade referencial.
- [ ] **EXPLAIN PLAN / ANALYZE** – Diagnosticar e otimizar performance de queries.

## 🧠 SQL Avançado
- [ ] **PIVOT / UNPIVOT** – Transformar linhas em colunas e vice-versa.
- [ ] **UDFs (User Defined Functions)** – Criar funções customizadas em SQL ou integradas com Python.
- [ ] **Views e Materialized Views** – Criar camadas reutilizáveis de consulta.
- [ ] **Tabelas Temporárias e Persistentes** – Gerenciar escopo e duração de dados intermediários.

---

