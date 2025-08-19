import numpy as np
import pandas as pd

from utils import *
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from boruta import BorutaPy
from sklearn.impute import SimpleImputer
from typing import Tuple, Optional  # Padronização de saída das funções


def remove_features_na(
    df: pd.DataFrame,
    threshold: float = 0.9,
    target_col: str = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Remove colunas de um DataFrame que excedem uma proporção de valores ausentes (NaNs).
    Ignora a variável target, se especificada.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame de entrada com variáveis a serem avaliadas.
    threshold : float, default=0.9
        Proporção máxima de valores ausentes permitida para manter a coluna.
    target_col : str, default=None
        Nome da coluna da variável resposta que é ignorada para remoção de variáveis.

    Retorna
    -------
    pd.DataFrame
        DataFrame com colunas removidas conforme critério.
    list[str]
        Lista com nomes das colunas removidas.
    """

    if target_col not in df.columns:
        raise ValueError(f"Coluna alvo '{target_col}' não encontrada no DataFrame.")

    if not 0 <= threshold <= 1:
        raise ValueError("threshold deve estar entre 0 e 1.")

    # Calcula a razão de missing, excluindo a coluna target (se houver)
    cols_to_check = df.columns.drop(target_col) if target_col in df.columns else df.columns
    na_ratio = df[cols_to_check].isnull().mean()

    # Seleciona colunas com missing acima do limite
    features_removidas = na_ratio[na_ratio > threshold].index.tolist()

    df_filtrado = df.drop(columns=features_removidas)

    # Relatório com o motivo da remoção das colunas
    df_relatorio = pd.DataFrame({
        "Features": features_removidas,
        "Status": "Removida",
        "Motivo da Remoção": f"Missing acima de {threshold:.1%}",
        "Importância (se aplicável)": None,
        "Descrição": [f"Porcentagem de NA da coluna é de : {na_ratio.loc[col]:.1%}." for col in features_removidas]
    })

    return df_filtrado, df_relatorio


def remove_features_sem_variacao_percentil(
    df: pd.DataFrame,
    p: float = 0.01,
    target_col: str = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Remove colunas do DataFrame em que o percentil `p` é igual ao percentil `1 - p`,
    indicando ausência de variação significativa na distribuição.

    Ignora a variável target, se especificada.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame de entrada com variáveis a serem avaliadas.
    p : float, default=0.01
        Valor de percentil usado na checagem (ex: 0.25 para Q1 == Q3).
    target_col : str, default=None
        Nome da coluna da variável resposta que é ignorada para remoção de variáveis.

    Retorna
    -------
    pd.DataFrame
        DataFrame com colunas removidas conforme critério.
    list[str]
        Lista com nomes das colunas removidas.
    """
    if target_col not in df.columns:
        raise ValueError(f"Coluna alvo '{target_col}' não encontrada no DataFrame.")

    if not 0 < p < 0.5:
        raise ValueError("O valor de p deve estar entre 0 e 0.5 (ex: 0.25).")

    # Seleção das variáveis numéricas
    cols_to_check = df.columns.drop(target_col) if target_col in df.columns else df.columns
    numeric_cols = df[cols_to_check].select_dtypes(include='number')

    # percentis das variáveis numéricas
    q_low = numeric_cols.quantile(p)
    q_high = numeric_cols.quantile(1 - p)

    # Colunas removidas
    features_removidas = q_low[q_low == q_high].index.tolist()
    df_filtrado = df.drop(columns=features_removidas)

    # Relatório
    df_relatorio = pd.DataFrame({
        "Features": features_removidas,
        "Status": "Removida",
        "Motivo da Remoção": f"Percentis iguais (P{p*100:.0f} = P{(1 - p)*100:.0f})",
        "Importância (se aplicável)": None,
        "Descrição": [f"Percentil P{p*100:.0f} igual ao P{(1 - p)*100:.0f} (valor = {q_low[col]})" for col in features_removidas]
    })

    return df_filtrado, df_relatorio


def seleciona_top_features_information_gain(
    df: pd.DataFrame,
    target_col: str,
    importance_threshold: float,
    max_features: int = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Seleciona as top features com base no Information Gain (LightGBM),
    utilizando um limiar cumulativo e opcionalmente um limite superior.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame original contendo todas as variáveis.
    target_col : str
        Nome da coluna target (variável resposta).
    importance_threshold : float
        Limite cumulativo de ganho de informação (entre 0 e 1).
    max_features : int, opcional
        Número máximo de features a manter.

    Retorna
    -------
    pd.DataFrame
        DataFrame contendo apenas as variáveis selecionadas.
    pd.DataFrame
        Relatório das variáveis removidas com justificativa.
    """

    if not 0 < importance_threshold <= 1:
        raise ValueError("O threshold deve estar entre 0 e 1.")

    # Calcula importâncias
    feature_importance_df = calcula_feature_importance(df, target_col)

    # Features abaixo do threshold
    top_threshold_df = feature_importance_df[
        feature_importance_df['Cumulative Importance Gain'] <= importance_threshold
    ]

    # Aplica limite de max_features, se especificado
    if max_features is not None:
        top_features_df = top_threshold_df.head(max_features)
    else:
        top_features_df = top_threshold_df

    selected_features = top_features_df['Feature'].tolist()
    df_filtrado = df[selected_features + [target_col]] if target_col in df.columns else df[selected_features]

    # Features removidas
    features_removidas_df = feature_importance_df[
        ~feature_importance_df['Feature'].isin(selected_features)
    ]

    # Gera descrição customizada
    descricoes = []
    for _, row in features_removidas_df.iterrows():
        split_pct = row['Relative Importance Split']
        gain_pct = row['Relative Importance Gain']
        feature = row['Feature']

        if max_features is not None and feature in top_threshold_df['Feature'].values:
            motivo = (
                "Feature estava entre as mais informativas (dentro do threshold de "
                f"{importance_threshold:.0%}), mas foi removida por limite de {max_features} variáveis."
            )
        else:
            motivo = (
                f"A variável representa {split_pct:.2%} dos splits do modelo e possui "
                f"Information Gain relativo de {gain_pct:.2%}."
            )

        descricoes.append(motivo)

    # Relatório final
    df_relatorio = pd.DataFrame({
        "Features": features_removidas_df['Feature'],
        "Status": "Removida",
        "Motivo da Remoção": [
            f"Fora do Top {importance_threshold:.0%} de Information Gain" if f not in top_threshold_df['Feature'].values
            else f"Fora do Top {max_features} de Information Gain, removida por corte manual"
            for f in features_removidas_df['Feature']
        ],
        "Importância (se aplicável)": features_removidas_df['Relative Importance Gain'].round(4),
        "Descrição": descricoes
    })

    return df_filtrado, df_relatorio


def remover_variaveis_correlacionadas(
    df: pd.DataFrame,
    target_col: str,
    corr_threshold: float = 0.5,
    method: str = 'pearson'
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Remove variáveis altamente correlacionadas, mantendo a com maior importância relativa.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame de entrada com variáveis a serem avaliadas.
    target_col : str
        Nome da coluna da variável resposta.
    corr_threshold : float, default=0.5
        Limite de correlação acima do qual uma das variáveis será removida. Definir em valor absoluto entre 0 e 1.
    method : str, default='pearson'
        Método de correlação a ser utilizado ('pearson', 'spearman' ou 'kendall').

    Retorna
    -------
    pd.DataFrame
        DataFrame com as variáveis restantes após a remoção.
    pd.DataFrame
        Relatório com informações sobre as variáveis removidas.
    """

    if method not in ['pearson', 'spearman', 'kendall']:
        raise ValueError("Método deve ser 'pearson', 'spearman' ou 'kendall'.")

    if not (0 < corr_threshold < 1):
        raise ValueError("corr_threshold deve estar entre 0 e 1 (exclusivo).")

    # Calcula importância relativa das features
    feature_importance_df = calcula_feature_importance(df, target_col)
    importance_map = feature_importance_df.set_index('Feature')['Relative Importance Gain'].to_dict()

    # Matriz de correlação sem a variável alvo
    df_corr = df.drop(columns=[target_col], errors='ignore').corr(method=method)
    cols = df_corr.columns.tolist()

    # Garante ordem de importância
    ordered_cols = [col for col in feature_importance_df['Feature'] if col in df_corr.columns]
    df_corr = df_corr[ordered_cols].loc[ordered_cols]

    # Máscara superior da matriz
    mask_upper = np.triu(np.ones(df_corr.shape), k=1).astype(bool)
    upper = pd.DataFrame(df_corr.values, columns=df_corr.columns, index=df_corr.index).where(mask_upper)

    # Inicialização
    # Inicializa o conjunto de variáveis a remover e o relatório
    features_removidas = set()
    relatorio = []

    # Percorre a matriz de correlação superior (apenas pares únicos)
    for col in upper.columns:
        for row in upper.index:
            corr_value = upper.loc[row, col]
            # Se a correlação for válida e acima do threshold definido
            if pd.notna(corr_value) and abs(corr_value) > corr_threshold:
                # Ignora pares já marcados para remoção
                if row in features_removidas or col in features_removidas:
                    continue

                # Obtém a importância relativa de cada variável do par
                imp_row = importance_map.get(row, 0)
                imp_col = importance_map.get(col, 0)

                # Define qual variável remover: mantém a de maior importância
                if imp_row >= imp_col:
                    drop_var, keep_var = col, row
                    imp_drop, imp_keep = imp_col, imp_row
                else:
                    drop_var, keep_var = row, col
                    imp_drop, imp_keep = imp_row, imp_col

                features_removidas.add(drop_var)
                relatorio.append({
                    "Features": drop_var,
                    "Status": "Removida",
                    "Motivo da Remoção": "Alta Correlação ({} > {:.0%})".format(method.capitalize(), corr_threshold),
                    "Importância (se aplicável)": round(imp_drop, 4),
                    "Descrição": f"Correlacionada com {keep_var} ({corr_value:.1%}). "
                                 f"InfoGain: {drop_var}={imp_drop:.1%}, {keep_var}={imp_keep:.1%}"
                })

    df_resultado = df.drop(columns=list(features_removidas), errors='ignore')
    df_relatorio = pd.DataFrame(relatorio)

    return df_resultado, df_relatorio


def selecionar_features_boruta(
    df: pd.DataFrame,
    target_col: str,
    max_iter: int = 100,
    random_state: int = 42,
    verbose: int = 1
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Aplica o algoritmo Boruta para seleção de variáveis.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame contendo as variáveis preditoras e a variável alvo.
    target_col : str
        Nome da coluna da variável resposta.
    max_iter : int, default=100
        Número máximo de iterações do algoritmo Boruta.
    random_state : int, default=42
        Semente para reprodutibilidade.
    verbose : int, default=1
        Nível de verbosidade (0 = silencioso, 1 = resumo, 2 = detalhado).

    Retorna
    -------
    pd.DataFrame
        DataFrame com as variáveis restantes após a remoção.
    pd.DataFrame
        Relatório com informações sobre as variáveis removidas.
    """

    if target_col not in df.columns:
        raise ValueError(f"Coluna alvo '{target_col}' não encontrada no DataFrame.")

    # Separa X e y
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # Imputação de Missing
    imputer = SimpleImputer(strategy='median')  # ou 'mean', 'most_frequent'
    X = imputer.fit_transform(X)

    if y.nunique() == 2:
        modelo = RandomForestClassifier(
            n_estimators=100,  # Mais estável para o shadow sampling
            max_depth=7,  # Controla overfitting
            n_jobs=-1,
            random_state=random_state
        )
    else:
        modelo = RandomForestRegressor(
            n_estimators=100,  # Mais estável para o shadow sampling
            max_depth=7,  # Controla overfitting
            n_jobs=-1,
            random_state=random_state
        )

    # Inicia e faz a seleção utilizando o método boruta
    boruta_selector = BorutaPy(
        estimator=modelo,
        n_estimators='auto',
        verbose=verbose,
        max_iter=max_iter,
        random_state=random_state
    )

    boruta_selector.fit(X, y)

    # Seleciona apenas as features realmente recomendadas pelo Boruta
    selected_features = df.drop(columns=[target_col]).columns[boruta_selector.support_].tolist() + [target_col]
    df_filtrado = df.loc[:, selected_features]

    features_removidas = df.drop(columns=[target_col]).columns[~boruta_selector.support_].tolist()

    df_relatorio = pd.DataFrame({
        "Features": features_removidas,
        "Status": "Removida",
        "Motivo da Remoção": "Boruta",
        "Importância (se aplicável)": None,
        "Descrição": "Variável removida pelo método Boruta utilizando RandomForest"
    })

    return df_filtrado, df_relatorio


def relatorio_selecionadas(
    df: pd.DataFrame,
    target_col: str
) -> pd.DataFrame:
    """
    Gera relatório para variáveis selecionadas com suas importâncias relativas.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame com as variáveis preditoras e a variável resposta.
    target_col : str, opcional
        Nome da coluna da variável resposta, usada para exclusão no cálculo de importância.

    Retorna
    -------
    pd.DataFrame
        Relatório contendo as features selecionadas e seus metadados.
    """
    
    feature_importance_df = calcula_feature_importance(df, target_col)

    df_relatorio = pd.DataFrame({
        "Features": feature_importance_df['Feature'],
        "Status": "Selecionada",
        "Motivo da Remoção": None,
        "Importância (se aplicável)": feature_importance_df['Relative Importance Gain'].round(4),
        "Descrição": "Variável selecionada durante a esteira de seleção de features"
    })

    return df_relatorio