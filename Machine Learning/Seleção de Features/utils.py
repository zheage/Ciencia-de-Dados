import pandas as pd
from lightgbm import LGBMClassifier, LGBMRegressor

def calcula_feature_importance(
    df: pd.DataFrame,
    target_col: str
) -> pd.DataFrame:
    """
    Calcula a importância das features utilizando o modelo LightGBM.

    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados de entrada.
    target_col (str): Nome da coluna alvo.

    Retorna:
    pd.DataFrame: DataFrame contendo a importância das features com base no número de splits e ganho.
    """

    if target_col not in df.columns:
        raise ValueError(f"Coluna alvo '{target_col}' não encontrada no DataFrame.")

    X = df.drop(columns = [target_col])
    y = df[target_col]

    if y.nunique() == 2:
        model = LGBMClassifier(
            n_estimators=1000,        # Número de árvores do modelo. Padrão é 100
            learning_rate=0.05,       # Taxa de aprendizagem. Padrão é 0.1
            num_leaves=31,            # Quantidade máxima de folhas de cada árvore do modelo
            max_depth=5,              # Profundidade máxima de cada árvore. Padrão é -1 (não há limite)
            subsample=0.7,            # Amostra da população utilizada em cada árvore, ajuda na robustez das importâncias (padrão é 1)
            colsample_bytree=0.7,     # Colunas utilizadas em cada árvore, garante que todas as variáveis tenham chance de ser testadas
            min_data_in_leaf=100,     # Quantidade mínima de instâncias por folha, evita splits pequenos
            random_state=42,          # Semente do modelo, para fins de reprodutibilidade
            verbosity=-1
        )
    else:
        model = LGBMRegressor(
            n_estimators=1000,        # Número de árvores do modelo. Padrão é 100
            learning_rate=0.05,       # Taxa de aprendizagem. Padrão é 0.1
            num_leaves=31,            # Quantidade máxima de folhas de cada árvore do modelo
            max_depth=5,              # Profundidade máxima de cada árvore. Padrão é -1 (não há limite)
            subsample=0.7,            # Amostra da população utilizada em cada árvore, ajuda na robustez das importâncias (padrão é 1)
            colsample_bytree=0.7,     # Colunas utilizadas em cada árvore, garante que todas as variáveis tenham chance de ser testadas
            min_data_in_leaf=100,     # Quantidade mínima de instâncias por folha, evita splits pequenos
            random_state=42,          # Semente do modelo, para fins de reprodutibilidade
            verbosity=-1
        )

    model.fit(X, y)

    feature_importance_df = pd.DataFrame({
        'Feature' : X.columns,
        'Feature Importance Split' :  model.booster_.feature_importance(importance_type='split'),
        'Feature Importance Gain' :   model.booster_.feature_importance(importance_type='gain')
    })

    # Ordena por Information Gain
    feature_importance_df.sort_values(by='Feature Importance Gain', ascending=False, inplace=True)
    feature_importance_df.reset_index(drop=True, inplace=True)

    # Importâncias relativas e acumuladas
    total_gain = feature_importance_df['Feature Importance Gain'].sum()
    total_split = feature_importance_df['Feature Importance Split'].sum()

    feature_importance_df['Relative Importance Gain'] = feature_importance_df['Feature Importance Gain'] / total_gain
    feature_importance_df['Relative Importance Split'] = feature_importance_df['Feature Importance Split'] / total_split
    feature_importance_df['Cumulative Importance Gain'] = feature_importance_df['Relative Importance Gain'].cumsum()


    return feature_importance_df