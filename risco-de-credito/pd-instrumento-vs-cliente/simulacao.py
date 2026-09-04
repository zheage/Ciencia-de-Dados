"""Simulação: PD estimada a nível instrumento vs a nível cliente.

Gera uma carteira sintética de varejo (clientes com 1 a 5 contratos), marca o
default sob duas definições (no contrato ou no cliente com arrasto), treina uma
regressão logística em cada granularidade e compara desempenho, calibração e
PD média atribuída ao contrato. A segunda parte simula um painel mensal para a
seção de análise de sobrevivência.

Saída: resultados.json, consumido por build_html.py.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve

SEED = 4966
N_CLIENTES = 30_000
PRODUTOS = ["consignado", "cdc_veiculo", "cartao", "credito_pessoal"]
INTERCEPTO_PRODUTO = {"consignado": -6.9, "cdc_veiculo": -6.3, "cartao": -4.9, "credito_pessoal": -5.0}
LGD_PRODUTO = {"consignado": 0.35, "cdc_veiculo": 0.40, "cartao": 0.75, "credito_pessoal": 0.70}
TICKET_MEDIO = {"consignado": 18_000, "cdc_veiculo": 35_000, "cartao": 4_000, "credito_pessoal": 9_000}
RHOS = [0.2, 0.5, 0.8]


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


# ----------------------------------------------------------------------------
# Parte 1: carteira, dois modelos, comparação
# ----------------------------------------------------------------------------
def gerar_carteira(rng: np.random.Generator) -> tuple[pd.DataFrame, pd.DataFrame]:
    z = rng.normal(size=N_CLIENTES)  # fator latente de risco do cliente
    renda = np.exp(rng.normal(8.2, 0.5, N_CLIENTES))
    score = np.clip(650 - 90 * z + rng.normal(0, 45, N_CLIENTES), 300, 1000)
    n_contratos = np.minimum(1 + rng.poisson(0.9, N_CLIENTES), 5)
    clientes = pd.DataFrame(
        {"id_cliente": np.arange(N_CLIENTES), "z": z, "renda": renda, "score": score, "n_contratos": n_contratos}
    )

    idx = np.repeat(clientes.index.values, n_contratos)
    n = len(idx)
    produto = rng.choice(PRODUTOS, size=n, p=[0.30, 0.20, 0.30, 0.20])
    ticket = np.array([TICKET_MEDIO[p] for p in produto]) * np.exp(rng.normal(0, 0.4, n))
    prazo = rng.choice([12, 24, 36, 48, 60], size=n, p=[0.15, 0.30, 0.30, 0.15, 0.10])
    parcela_renda = np.clip(ticket / prazo / (clientes.renda.values[idx] / 12), 0.01, 1.5)
    idade_contrato = rng.integers(0, 24, n)
    contratos = pd.DataFrame(
        {
            "id_cliente": idx,
            "produto": produto,
            "saldo": ticket,
            "prazo": prazo,
            "parcela_renda": parcela_renda,
            "idade_contrato": idade_contrato,
            "z": clientes.z.values[idx],
            "score": clientes.score.values[idx],
            "renda": clientes.renda.values[idx],
            "n_contratos": n_contratos[idx],
        }
    )
    return clientes, contratos


def marcar_default(contratos: pd.DataFrame, rho: float, rng: np.random.Generator) -> pd.DataFrame:
    """Logit do contrato = intercepto do produto + efeito de features + fator comum (cliente) + idiossincrático.

    rho controla a fração da variância latente compartilhada pelos contratos do mesmo cliente.
    """
    c = contratos.copy()
    eps = rng.normal(size=len(c))
    latente = np.sqrt(rho) * c.z.values + np.sqrt(1 - rho) * eps
    logit = (
        c.produto.map(INTERCEPTO_PRODUTO).values
        + 2.2 * np.log1p(c.parcela_renda.values)
        + 0.15 * (c.prazo.values / 12)
        - 0.02 * np.abs(c.idade_contrato.values - 9)  # efeito de maturação: pico perto do mês 9
        + 1.4 * latente
    )
    c["pd_verdadeira"] = sigmoid(logit)
    c["default_contrato"] = (rng.uniform(size=len(c)) < c.pd_verdadeira).astype(int)
    c["default_cliente"] = c.groupby("id_cliente").default_contrato.transform("max")
    c["lgd"] = c.produto.map(LGD_PRODUTO)
    return c


def features_contrato(c: pd.DataFrame) -> pd.DataFrame:
    x = pd.DataFrame(
        {
            "score": (c.score - 650) / 100,
            "log_renda": np.log(c.renda) - 8.2,
            "log_parcela_renda": np.log1p(c.parcela_renda),
            "prazo_anos": c.prazo / 12,
            "idade_contrato": c.idade_contrato / 12,
            "n_contratos": c.n_contratos,
        }
    )
    for p in PRODUTOS[1:]:
        x[f"prod_{p}"] = (c.produto == p).astype(int)
    return x


def features_cliente(c: pd.DataFrame) -> pd.DataFrame:
    g = c.groupby("id_cliente")
    x = pd.DataFrame(
        {
            "score": (g.score.first() - 650) / 100,
            "log_renda": np.log(g.renda.first()) - 8.2,
            "max_log_parcela_renda": np.log1p(g.parcela_renda.max()),
            "soma_parcela_renda": g.parcela_renda.sum(),
            "log_saldo_total": np.log(g.saldo.sum()),
            "prazo_max_anos": g.prazo.max() / 12,
            "n_contratos": g.size(),
        }
    )
    flags = pd.crosstab(c.id_cliente, c.produto).clip(upper=1).reindex(columns=PRODUTOS, fill_value=0)
    for p in PRODUTOS:
        x[f"tem_{p}"] = flags[p].reindex(x.index).fillna(0).astype(int)
    return x


def ks_stat(y: np.ndarray, p: np.ndarray) -> float:
    fpr, tpr, _ = roc_curve(y, p)
    return float(np.max(tpr - fpr))


def curva_roc(y: np.ndarray, p: np.ndarray, n_pts: int = 60) -> list[list[float]]:
    fpr, tpr, _ = roc_curve(y, p)
    grid = np.linspace(0, 1, n_pts)
    return [[float(a), float(b)] for a, b in zip(grid, np.interp(grid, fpr, tpr))]


def calibracao(y: np.ndarray, p: np.ndarray, n_bins: int = 10) -> list[dict]:
    q = pd.qcut(pd.Series(p).rank(method="first"), n_bins, labels=False)
    out = []
    for b in range(n_bins):
        m = q == b
        out.append({"decil": b + 1, "previsto": float(p[m].mean()), "observado": float(y[m].mean()), "n": int(m.sum())})
    return out


def histograma(p: np.ndarray, edges: np.ndarray) -> list[float]:
    h, _ = np.histogram(p, bins=edges)
    return (h / h.sum()).round(5).tolist()


@dataclass
class Cenario:
    marcacao: str  # "contrato" ou "cliente"
    rho: float


def rodar_cenario(
    cen: Cenario, contratos_base: pd.DataFrame, rng: np.random.Generator, teste_ids: set[int], ids_exemplo: list[int]
) -> dict:
    c = marcar_default(contratos_base, cen.rho, rng)
    alvo = "default_contrato" if cen.marcacao == "contrato" else "default_cliente"

    # split por cliente: contratos do mesmo cliente nunca ficam em treino e teste ao mesmo tempo
    c["teste"] = c.id_cliente.isin(teste_ids)

    # modelo a nível instrumento
    xi = features_contrato(c)
    m_i = LogisticRegression(max_iter=2000, C=10.0)
    m_i.fit(xi[~c.teste], c.loc[~c.teste, alvo])
    c["pd_instrumento"] = m_i.predict_proba(xi)[:, 1]

    # modelo a nível cliente, PD atribuída a todos os contratos do cliente
    xc = features_cliente(c)
    y_cli = c.groupby("id_cliente").default_cliente.max()
    treino_cli = ~xc.index.isin(list(teste_ids))
    m_c = LogisticRegression(max_iter=2000, C=10.0)
    m_c.fit(xc[treino_cli], y_cli[treino_cli])
    pd_cli = pd.Series(m_c.predict_proba(xc)[:, 1], index=xc.index)
    c["pd_cliente"] = c.id_cliente.map(pd_cli)

    t = c[c.teste].copy()
    y = t[alvo].values
    res: dict = {"marcacao": cen.marcacao, "rho": cen.rho, "n_contratos_teste": int(len(t)), "taxa_default": float(y.mean())}

    for nome, col in [("instrumento", "pd_instrumento"), ("cliente", "pd_cliente")]:
        p = t[col].values
        res[nome] = {
            "pd_media": float(p.mean()),
            "auc": float(roc_auc_score(y, p)),
            "gini": float(2 * roc_auc_score(y, p) - 1),
            "ks": ks_stat(y, p),
            "brier": float(np.mean((p - y) ** 2)),
            "roc": curva_roc(y, p),
            "calibracao": calibracao(y, p),
            "ecl": float((p * t.lgd * t.saldo).sum()),
            "pd_por_n_contratos": [float(p[t.n_contratos.values == k].mean()) for k in range(1, 6)],
            "pd_por_produto": {pr: float(p[t.produto.values == pr].mean()) for pr in PRODUTOS},
        }

    edges = np.concatenate([[0], np.geomspace(0.005, 0.6, 24), [1]])
    res["hist_edges"] = edges.round(5).tolist()
    res["hist"] = {
        "instrumento": histograma(t.pd_instrumento.values, edges),
        "cliente": histograma(t.pd_cliente.values, edges),
    }
    res["observado"] = {
        "por_n_contratos": [float(y[t.n_contratos.values == k].mean()) for k in range(1, 6)],
        "n_por_n_contratos": [int((t.n_contratos.values == k).sum()) for k in range(1, 6)],
        "por_produto": {pr: float(y[t.produto.values == pr].mean()) for pr in PRODUTOS},
        "perda": float((y * t.lgd * t.saldo).sum()),
        "ead_total": float(t.saldo.sum()),
    }
    # dispersão intra-cliente: para clientes com 2+ contratos, amplitude das PDs de instrumento
    multi = t[t.n_contratos >= 2].groupby("id_cliente").pd_instrumento.agg(["min", "max"])
    res["dispersao_intra_cliente"] = {
        "amplitude_mediana": float((multi["max"] - multi["min"]).median()),
        "razao_mediana": float((multi["max"] / multi["min"]).median()),
    }
    # amostra para scatter PD cliente x PD instrumento
    amostra = t.sample(1500, random_state=1)
    res["scatter"] = [
        [round(float(a), 4), round(float(b), 4), int(k)]
        for a, b, k in zip(amostra.pd_instrumento, amostra.pd_cliente, amostra.n_contratos)
    ]
    # clientes de exemplo (4 ou 5 contratos, holdout) para a tabela de PD por contrato e por cliente
    res["exemplos"] = []
    for cid in ids_exemplo:
        g = c[c.id_cliente == cid].sort_values("idade_contrato", ascending=False)
        if g.default_cliente.iloc[0] == 0:
            continue
        res["exemplos"].append(
            {
                "id": int(cid),
                "score": int(round(g.score.iloc[0])),
                "renda": round(float(g.renda.iloc[0])),
                "default_cliente": int(g.default_cliente.iloc[0]),
                "pd_cliente": round(float(g.pd_cliente.iloc[0]), 4),
                "contratos": [
                    {
                        "produto": r.produto,
                        "saldo": round(float(r.saldo)),
                        "prazo": int(r.prazo),
                        "parcela_renda": round(float(r.parcela_renda), 3),
                        "idade": int(r.idade_contrato),
                        "default_contrato": int(r.default_contrato),
                        "default_arrasto": int(r.default_cliente),
                        "pd_instrumento": round(float(r.pd_instrumento), 4),
                        "lgd": float(r.lgd),
                    }
                    for r in g.itertuples()
                ],
            }
        )
    return res


# ----------------------------------------------------------------------------
# Parte 2: painel mensal para análise de sobrevivência
# ----------------------------------------------------------------------------
HORIZONTE = 36


def hazard_contrato(idade: np.ndarray, mult: np.ndarray) -> np.ndarray:
    """Hazard mensal do contrato em função da idade (efeito de maturação: sobe, pico ~mês 8, cai)."""
    base = 0.0025 + 0.011 * (idade / 8.0) * np.exp(1 - idade / 8.0)
    return np.clip(base * mult, 0, 0.5)


def simular_painel(rng: np.random.Generator, n_cli: int = 15_000) -> dict:
    z = rng.normal(size=n_cli)
    score = np.clip(650 - 90 * z + rng.normal(0, 45, n_cli), 300, 1000)
    mult = np.exp(0.9 * z)
    faixa = np.where(score >= 700, "baixo", np.where(score >= 580, "medio", "alto"))

    # contratos por cliente com origem escalonada dentro do relacionamento
    n_ctr = np.minimum(1 + rng.poisson(1.0, n_cli), 4)
    inicio, fim, cli = [], [], []
    for i in range(n_cli):
        starts = np.sort(np.concatenate([[0], rng.integers(1, 30, n_ctr[i] - 1)])) if n_ctr[i] > 1 else np.array([0])
        prazos = rng.choice([6, 12, 24, 36, 48], size=n_ctr[i], p=[0.15, 0.25, 0.30, 0.20, 0.10])
        # pré-pagamento informativo: cliente de baixo risco liquida antes com mais frequência
        p_prepag = np.clip(0.45 - 0.15 * z[i], 0.05, 0.8)
        prep = rng.uniform(size=n_ctr[i]) < p_prepag
        prazos = np.where(prep, np.maximum(3, (prazos * rng.uniform(0.3, 0.8, n_ctr[i])).astype(int)), prazos)
        inicio.extend(starts.tolist())
        fim.extend((starts + prazos).tolist())
        cli.extend([i] * n_ctr[i])
    inicio, fim, cli = np.array(inicio), np.array(fim), np.array(cli)

    # evolução mensal
    t_default_cli = np.full(n_cli, -1)
    t_saida_cli = np.full(n_cli, HORIZONTE)  # mês em que o último contrato encerra (censura)
    ultimo_fim = pd.Series(fim).groupby(cli).max().values
    t_saida_cli = np.minimum(ultimo_fim, HORIZONTE)

    # instrumento: default próprio por contrato
    t_default_ctr = np.full(len(cli), -1)
    hazard_por_idade = np.zeros(HORIZONTE)
    expostos_por_idade = np.zeros(HORIZONTE)
    hazard_por_tempo_cli = np.zeros(HORIZONTE)
    expostos_por_tempo_cli = np.zeros(HORIZONTE)
    vivo_cli = np.ones(n_cli, bool)
    for t in range(HORIZONTE):
        ativo = (inicio <= t) & (t < fim) & (t_default_ctr < 0) & vivo_cli[cli]
        idade = t - inicio
        h = hazard_contrato(idade.astype(float), mult[cli])
        u = rng.uniform(size=len(cli))
        cai = ativo & (u < h)
        # hazard empírico por idade do contrato (instrumento)
        for a in np.unique(idade[ativo]):
            m = ativo & (idade == a)
            if 0 <= a < HORIZONTE:
                expostos_por_idade[a] += m.sum()
                hazard_por_idade[a] += cai[m].sum()
        t_default_ctr[cai] = t
        # cliente: arrasto, primeiro default de qualquer contrato encerra o cliente
        cli_ativo = vivo_cli & (t < t_saida_cli) & (np.bincount(cli[ativo], minlength=n_cli) > 0)
        cli_cai = np.zeros(n_cli, bool)
        cli_cai[np.unique(cli[cai])] = True
        cli_cai &= cli_ativo
        expostos_por_tempo_cli[t] += cli_ativo.sum()
        hazard_por_tempo_cli[t] += cli_cai.sum()
        t_default_cli[cli_cai] = t
        vivo_cli &= ~cli_cai

    # Kaplan-Meier a nível cliente por faixa de risco, com censura na saída
    evento = t_default_cli >= 0
    tempo = np.where(evento, t_default_cli + 1, t_saida_cli)
    km_por_faixa = {}
    naive_por_faixa = {}
    for f in ["baixo", "medio", "alto"]:
        m = faixa == f
        km_por_faixa[f] = kaplan_meier(tempo[m], evento[m])
        n0 = m.sum()
        naive_por_faixa[f] = [float(((t_default_cli[m] >= 0) & (t_default_cli[m] < t)).sum() / n0) for t in range(1, HORIZONTE + 1)]
    km_total = kaplan_meier(tempo, evento)
    naive_total = [float(((t_default_cli >= 0) & (t_default_cli < t)).sum() / n_cli) for t in range(1, HORIZONTE + 1)]

    # hazard discreto estimado por regressão logística pessoa-período (cliente), por faixa
    linhas = []
    for i in range(n_cli):
        fim_obs = int(tempo[i])
        for t in range(fim_obs):
            linhas.append((t, faixa[i], 1 if (evento[i] and t == fim_obs - 1) else 0))
    pp = pd.DataFrame(linhas, columns=["t", "faixa", "y"])
    xpp = pd.get_dummies(pp[["t", "faixa"]].astype({"t": "category"}), drop_first=False).astype(float)
    mod = LogisticRegression(max_iter=3000, C=5.0).fit(xpp, pp.y)
    hz_modelo = {}
    for f in ["baixo", "medio", "alto"]:
        grid = pd.DataFrame({"t": pd.Categorical(range(HORIZONTE), categories=range(HORIZONTE)), "faixa": f})
        xg = pd.get_dummies(grid, drop_first=False).reindex(columns=xpp.columns, fill_value=0).astype(float)
        hz_modelo[f] = mod.predict_proba(xg)[:, 1].round(5).tolist()

    with np.errstate(divide="ignore", invalid="ignore"):
        hz_idade = np.where(expostos_por_idade > 0, hazard_por_idade / expostos_por_idade, np.nan)
        hz_tempo = np.where(expostos_por_tempo_cli > 0, hazard_por_tempo_cli / expostos_por_tempo_cli, np.nan)

    # PD 12 meses derivada da curva: 1 - S(12)
    return {
        "horizonte": HORIZONTE,
        "km": {**km_por_faixa, "total": km_total},
        "naive": {**naive_por_faixa, "total": naive_total},
        "hazard_idade_contrato": [None if np.isnan(v) else round(float(v), 5) for v in hz_idade],
        "hazard_tempo_cliente": [None if np.isnan(v) else round(float(v), 5) for v in hz_tempo],
        "expostos_idade_contrato": expostos_por_idade.astype(int).tolist(),
        "expostos_tempo_cliente": expostos_por_tempo_cli.astype(int).tolist(),
        "hazard_modelo_faixa": hz_modelo,
        "n_clientes": int(n_cli),
        "n_contratos": int(len(cli)),
        "pct_censurados": float(1 - evento.mean()),
        "pct_censura_antes_horizonte": float(((~evento) & (t_saida_cli < HORIZONTE)).mean()),
        "pd12": {
            f: {"km": float(1 - km_por_faixa[f]["s"][11]), "naive": float(naive_por_faixa[f][11])}
            for f in ["baixo", "medio", "alto"]
        } | {"total": {"km": float(1 - km_total["s"][11]), "naive": float(naive_total[11])}},
        "pd36": {
            f: {"km": float(1 - km_por_faixa[f]["s"][35]), "naive": float(naive_por_faixa[f][35])}
            for f in ["baixo", "medio", "alto"]
        } | {"total": {"km": float(1 - km_total["s"][35]), "naive": float(naive_total[35])}},
        "n_por_faixa": {f: int((faixa == f).sum()) for f in ["baixo", "medio", "alto"]},
        "exemplo_timeline": exemplo_timeline(rng),
    }


def kaplan_meier(tempo: np.ndarray, evento: np.ndarray) -> dict:
    s, out_s, out_lo, out_hi = 1.0, [], [], []
    var_acum = 0.0
    for t in range(1, HORIZONTE + 1):
        em_risco = (tempo >= t).sum()
        d = ((tempo == t) & evento).sum()
        if em_risco > 0 and d > 0:
            s *= 1 - d / em_risco
            var_acum += d / (em_risco * (em_risco - d)) if em_risco > d else 0
        se = s * np.sqrt(var_acum)
        out_s.append(round(float(s), 5))
        out_lo.append(round(float(max(0, s - 1.96 * se)), 5))
        out_hi.append(round(float(min(1, s + 1.96 * se)), 5))
    return {"s": out_s, "lo": out_lo, "hi": out_hi}


def exemplo_timeline(rng: np.random.Generator) -> list[dict]:
    """Um cliente ilustrativo com três contratos para o diagrama de origem do tempo."""
    return [
        {"nome": "Consignado", "inicio": 0, "fim": 36, "status": "ativo"},
        {"nome": "Cartão", "inicio": 6, "fim": 20, "status": "default", "evento": 20},
        {"nome": "CDC veículo", "inicio": 14, "fim": 26, "status": "liquidado"},
    ]


def main() -> None:
    rng = np.random.default_rng(SEED)
    clientes, contratos = gerar_carteira(rng)
    rng_split = np.random.default_rng(SEED + 7)
    ids = clientes.id_cliente.values
    teste_ids = set(rng_split.choice(ids, size=int(0.4 * len(ids)), replace=False).tolist())
    candidatos = clientes[(clientes.n_contratos >= 4) & clientes.id_cliente.isin(teste_ids)].id_cliente.values
    ids_exemplo = rng_split.choice(candidatos, size=min(250, len(candidatos)), replace=False).tolist()
    cenarios = []
    for marcacao in ["contrato", "cliente"]:
        for rho in RHOS:
            cenarios.append(
                rodar_cenario(Cenario(marcacao, rho), contratos, np.random.default_rng(SEED + int(rho * 100)), teste_ids, ids_exemplo)
            )
    sobrevivencia = simular_painel(np.random.default_rng(SEED + 1))
    saida = {
        "meta": {
            "n_clientes": int(N_CLIENTES),
            "n_contratos": int(len(contratos)),
            "dist_n_contratos": clientes.n_contratos.value_counts().sort_index().to_dict(),
            "produtos": PRODUTOS,
            "lgd": LGD_PRODUTO,
            "rhos": RHOS,
            "seed": SEED,
        },
        "cenarios": cenarios,
        "sobrevivencia": sobrevivencia,
    }
    Path(__file__).with_name("resultados.json").write_text(json.dumps(saida, ensure_ascii=False))
    for c in cenarios:
        print(
            f"marcacao={c['marcacao']:8s} rho={c['rho']:.1f} taxa={c['taxa_default']:.3%} | "
            f"instr: pd={c['instrumento']['pd_media']:.3%} gini={c['instrumento']['gini']:.3f} ks={c['instrumento']['ks']:.3f} | "
            f"cli: pd={c['cliente']['pd_media']:.3%} gini={c['cliente']['gini']:.3f} ks={c['cliente']['ks']:.3f} | "
            f"ECL i/c={c['instrumento']['ecl']/1e6:.2f}/{c['cliente']['ecl']/1e6:.2f} obs={c['observado']['perda']/1e6:.2f}"
        )
    s = sobrevivencia
    print("PD12:", {k: (round(v['km'], 4), round(v['naive'], 4)) for k, v in s["pd12"].items()})
    print("PD36:", {k: (round(v['km'], 4), round(v['naive'], 4)) for k, v in s["pd36"].items()})
    print("censurados:", round(s["pct_censurados"], 3), "antes do horizonte:", round(s["pct_censura_antes_horizonte"], 3))


if __name__ == "__main__":
    main()
