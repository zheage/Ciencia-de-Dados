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

# 📚 Roadmap: Sistema Bancário e Ativos Financeiros

## 🏦 Fundamentos do Sistema Financeiro Nacional (SFN)
- [ ] Estrutura do SFN: CMN, BACEN, CVM, SUSEP, Previc
- [ ] Instituições financeiras: bancos comerciais, múltiplos, cooperativas, financeiras
- [ ] Papel do BACEN, CVM, SUSEP
- [ ] Sistema de Pagamentos Brasileiro (SPB)
  

## 📑 Relatórios de Impacto para Risco de Crédito

- [ ] Balanço Patrimonial
  - [Bradesco](https://www.bradescori.com.br/informacoes-ao-mercado/relatorios-e-planilhas/relatorios/) 
  - [Itaú](https://www.itau.com.br/relacoes-com-investidores/resultados-e-relatorios/central-de-resultados/)
  - [NuBank](https://nubank.com.br/transparencia/relatorios-financeiros)
- [ ] DRE (Demonstração do Resultado do Exercício)
- [ ] Notas Explicativas e Release de RI
- [ ] DLO (Demonstrativos de Limites Operacionais) 
- [ ] RAS (Relatório de Apetite ao Risco)
- [ ] PR (Patrimônio de Referência)
- [ ] RWA (Ativos Ponderados pelo Risco)
- [ ] Índice de Basiléia  
- [ ] CEA (Capital Econômico Alocado)

## 💰 Tipos de Ativos Financeiros
- [ ] Renda Fixa: CDB, LCI, LCA, Tesouro Direto, Debêntures
- [ ] Renda Variável: Ações, BDRs, ETFs, FIIs
- [ ] Derivativos: opções, futuros, swaps
- [ ] Criptoativos (noções introdutórias)

## 🏛️ Mercado Bancário
- [ ] Estrutura dos bancos no Brasil
- [ ] Produtos bancários: conta corrente, crédito, cartões
- [ ] Gestão de risco de crédito e inadimplência
- [ ] Spread bancário
- [ ] Gestão de risco de crédito

## 💵 Produtos de Captação (Passivos)

- [ ] Conta corrente e conta salário
- [ ] Caderneta de poupança (TR, liquidez, tributação)
- [ ] CDB/RDB (pré, pós, híbridos)
- [ ] LCI e LCA (lastros, isenção, prazos)
- [ ] DPGE – Depósito com Garantia Especial
- [ ] Cobertura do FGC e limites

## 💎 Produtos de Crédito (Ativos)

- [ ] Crédito pessoal e consignado
- [ ] Financiamentos (veículos, imóveis)
- [ ] Cartões de crédito e crédito rotativo
- [ ] Cheque especial
- [ ] Home equity
- [ ] SAC x PRICE
- [ ] CET (Custo Efetivo Total)
- [ ] Margem consignável

## Produtos de Investimento

- [ ] Fundos de Investimento (RF, Ações, Multimercado)
- [ ] Classificação ANBIMA de fundos
- [ ] Tesouro Direto (prefixado, Selic, IPCA+)
- [ ] Debêntures, CRI, CRA
- [ ] COE (Certificados de Operações Estruturadas)
- [ ] Previdência Privada (PGBL x VGBL, regimes de tributação)

## 🪙 Seguros, Capitalização e Consórcios

- [ ] Seguro de vida, residencial, prestamista
- [ ] Capitalização: como funciona, vantagens e riscos
- [ ] Consórcios: cartas de crédito e contemplação
- [ ] Produtos híbridos (investimentos + seguros)

## 🏦 Tributação, Perfil e Riscos

- [ ] Tributação de RF, fundos, ações e previdência
- [ ] IOF regressivo
- [ ] Come-cotas e regimes de fundos (curto/longo prazo)
- [ ] Suitability e perfil do investidor
- [ ] Resolução CVM 30 / ANBIMA Código de Varejo
- [ ] Avaliação de risco e compatibilidade de produto

## 📜 Regulação Bancária
- [ ] Resoluções do BACEN (ex: 4.966), IFRS9, Basileia III
- [ ] Supervisão e compliance bancário
- [ ] Sistema de garantias (FGC)

## 📐 Matemática Financeira e Valuation
- [ ] Juros simples e compostos
- [ ] Valor presente e valor futuro
- [ ] Duration, convexidade
- [ ] Valuation (DCF, Múltiplos)

## 📊 Economia e Política Monetária
- [ ] Inflação, juros, câmbio, PIB
- [ ] Selic, inflação, PIB
- [ ] Política monetária e fiscal

## 📈 Demonstrações Financeiras
- [ ] DRE, Balanço Patrimonial, DFC
- [ ] Indicadores: ROE, ROA, Índice de Basileia
- [ ] Análise fundamentalista e risco de crédito

## 🧠 Tecnologia e Inovação
- [ ] Pix, Open Finance, Open Banking
- [ ] Fintechs e bancos digitais
- [ ] Sandbox regulatório e APIs bancárias

## 🧱 Áreas de Atuação do Cientista de Dados

### 💼 1. Comercial / Produtos
- [ ] Precificação de produtos bancários
- [ ] Elasticidade de demanda, análise de canais
- [ ] Análise de rentabilidade por produto
- [ ] Segmentação de clientes por perfil de consumo

### 🧮 2. Crédito (Políticas, Estratégias, Precificação, Modelagem)
- [ ] Modelos de PD, LGD, EAD
- [ ] Segmentação de risco e definição de políticas de concessão
- [ ] IFRS 9 e BACEN 4966
- [ ] Scorecards, regressão logística, LightGBM, XGBoost

### 💳 3. Cobrança
- [ ] Modelos de propensão à recuperação
- [ ] Análise de canais e estratégias de cobrança
- [ ] Otimização de contingência
- [ ] Segmentações de inadimplência

### 📣 4. Marketing / CRM
- [ ] Modelagem de churn, LTV, campanhas de aquisição
- [ ] Segmentações comportamentais
- [ ] Modelos de recomendação e cross-sell
- [ ] Uplift modeling e análise de campanhas

### 📊 5. Riscos (Crédito, Mercado e Operacional)
- [ ] Estudo de VaR, CVaR e stress testing
- [ ] Modelagem de risco operacional (eventos, KRI)
- [ ] Cálculo de provisões (esperadas x inesperadas)
- [ ] Risco soberano, câmbio, liquidez

### 🔐 6. Prevenção à Fraude
- [ ] Modelos supervisionados e não supervisionados
- [ ] Análise de redes (graph analytics)
- [ ] Detecção em tempo real (streaming + alertas)
- [ ] Engenharia de variáveis comportamentais

### 🧾 7. Gestão de Carteira e Portfólio
- [ ] Painéis de monitoramento de indicadores (dashboards)
- [ ] Curvas de vintage, roll rate, aging
- [ ] Análise de dispersão e concentração de risco
- [ ] Segmentações de carteira

### 🛠️ 8. TI / Engenharia de Dados / MLOps / DevOps
- [ ] Arquitetura de dados (Data Lake, Delta Lake)
- [ ] Pipelines de ingestão (Airflow, Spark, DBT)
- [ ] Versionamento de modelos (MLflow, DVC)
- [ ] Infraestrutura em nuvem (Azure, AWS)

### 📈 9. MIS / BI / Portfólio
- [ ] Automatização de relatórios e rotinas
- [ ] Visualização de KPIs regulatórios e de negócio
- [ ] Power BI, Tableau, Metabase
- [ ] Modelagem de dados (dimensional, star schema)

### 💹 10. Investimento / Tesouraria / Mercado de Capitais
- [ ] Avaliação de derivativos, precificação de ativos
- [ ] Modelos de previsão de séries temporais financeiras
- [ ] Análise de risco de mercado e de liquidez
- [ ] Curvas de juros, duration, convexidade

### 📋 11. Compliance / Auditoria / Controles Internos
- [ ] Monitoramento de limites, alçadas e exceções
- [ ] LGPD, KYC, PLDFT
- [ ] Análises de aderência a normas (CVM, BACEN)
- [ ] Criação de trilhas de auditoria com logs e metadados

### 🧾 12. Contabilidade / Controladoria / Fiscal
- [ ] Impacto das provisões nos demonstrativos
- [ ] Consolidação de resultados contábeis
- [ ] Análise de IRPJ/CSLL e efeitos fiscais
- [ ] Entendimento do COSIF e plano contábil

### ⚖️ 13. Jurídico Contencioso
- [ ] Modelos de probabilidade de perda judicial
- [ ] Análise de litígios e clusters de ações
- [ ] Text mining de petições e decisões
- [ ] Suporte a provisionamento contábil

### 🚀 14. Inovação e Projetos de Dados
- [ ] Criação de protótipos e POCs com IA
- [ ] Automação com IA generativa e copilots
- [ ] Open Finance, Explainable AI (SHAP, LIME)
- [ ] Cultura analítica e transformação digital