# PD por instrumento ou por cliente

Simulação comparando PD 12 meses estimada a nível instrumento (uma linha por contrato) e a nível
cliente (uma linha por cliente, PD replicada nos contratos), sob duas definições de default:
marcação no contrato e marcação no cliente com arrasto. Inclui uma seção sobre análise de
sobrevivência quando a PD lifetime é construída a nível cliente (origem do tempo, censura
informativa, truncamento à esquerda, riscos competitivos, hazard discreto pessoa-período).

Resultado: [`pd_instrumento_vs_cliente.html`](./pd_instrumento_vs_cliente.html), página
autocontida com filtros (marcação do default e risco compartilhado ρ) e gráficos em SVG próprio.

## Reproduzir

```bash
pip install numpy pandas scipy scikit-learn
python simulacao.py      # gera resultados.json (~15 s)
python build_html.py     # injeta o JSON no template.html e gera o HTML final
```

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `simulacao.py` | Carteira sintética, marcação de default, dois modelos logísticos, métricas, painel mensal e Kaplan-Meier |
| `template.html` | Página, textos e biblioteca de gráficos SVG (placeholder `__DADOS__`) |
| `build_html.py` | Monta o HTML final |
| `resultados.json` | Saída da simulação com seed fixo |

## Principais conclusões

- Com default marcado no contrato, o modelo cliente superestima a PD de cada contrato e a
  superestimação cresce com o número de contratos do cliente (mede "algum contrato falha" e cola
  o número em todos). ECL sai mais que o dobro da perda observada.
- Com arrasto, as duas abordagens convergem no nível e o modelo cliente ganha um pouco de Gini;
  a diferença que resta é de coerência: o modelo instrumento dá PDs diferentes para contratos que
  respondem ao mesmo evento.
- Partição treino/teste sempre por cliente; sem isso o Gini do modelo instrumento sai inflado.
- Ignorar censura na PD lifetime de cliente subestima a PD, e a censura por liquidação é
  informativa (quem liquida tende a ser o de menor risco), o que Kaplan-Meier não corrige.
