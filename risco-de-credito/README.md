# 💳 Risco de Crédito

Anotações e implementações sobre modelagem de risco de crédito, com foco em Basileia, CMN 4.966/2021 e IFRS 9.

## Tópicos

### Modelagem (`modelagem/`)
- PD (Probabilidade de Default): scorecard, regressão logística
- LGD (Loss Given Default): modelos de recuperação
- EAD (Exposure at Default): CCF e modelos de utilização

### Validação (`validacao/`)
- KS, Gini e curva ROC
- PSI (Population Stability Index)
- Backtesting e stress test

### Regulatório (`regulatorio/`)
- CMN 4.966/2021 e IFRS 9
- Basileia II/III: abordagem IRB
- Provisionamento e ECL (Expected Credit Loss)

## Projetos (`pd-instrumento-vs-cliente/`)
- [PD por instrumento ou por cliente](./pd-instrumento-vs-cliente/): simulação comparando as duas granularidades sob marcação de default no contrato e no cliente, com seção de análise de sobrevivência para PD lifetime de cliente. Resultado em HTML interativo.
