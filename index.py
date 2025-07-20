# Pacotes principais
import pandas as pd
import matplotlib.pyplot as plt


# Configurações de visualização
plt.style.use("ggplot")


df_features_train = pd.read_csv('dengue_features_train.csv')
df_labels_train = pd.read_csv('dengue_labels_train.csv')
df_features_test = pd.read_csv('dengue_features_test.csv')
df_submission_format = pd.read_csv('submission_format.csv')

#juntar os parametros com o numero de casos efetivamente

df = df_features_train.merge(df_labels_train, on=["city", "year", "weekofyear"], how="left")


# 1. Mostrar cabeçalho (nomes das colunas)
print("\n🧾 Cabeçalho (colunas):")
print(list(df.columns))

# 2. Tipos de dados por coluna
print("\n🔢 Tipos de dados por coluna:")
print(df.dtypes)

# 3. Contagem de valores ausentes por coluna
print("\n⚠️ Valores ausentes por coluna:")
missing = df.isna().sum()
print(missing[missing > 0] if missing.sum() > 0 else "Nenhum valor ausente encontrado.")

# 4. Visualizar o início da tabela
print("\n🔍 Primeiras linhas da tabela:")
print(df.head())

# ✅ 1. Criar média de NDVI
df['ndvi_mean'] = df[['ndvi_ne', 'ndvi_nw', 'ndvi_se', 'ndvi_sw']].mean(axis=1)

# ✅ 2. Criar variável de dias secos consecutivos
dry_threshold = 1.0
df['dry_day'] = df['precipitation_amt_mm'] < dry_threshold
df['dry_days'] = df.groupby('city')['dry_day'].transform(
    lambda x: x.groupby((x != x.shift()).cumsum()).cumcount() + 1
)

# ✅ 3. Lista de colunas para lag
cols_to_lag = [
    'ndvi_mean',
    'precipitation_amt_mm',
    'station_precip_mm',
    'station_avg_temp_c',
    'station_max_temp_c',
    'station_min_temp_c',
    'reanalysis_air_temp_k',
    'reanalysis_avg_temp_k',
    'reanalysis_tdtr_k',
    'reanalysis_relative_humidity_percent',
    'reanalysis_specific_humidity_g_per_kg',
    'reanalysis_dew_point_temp_k',
    'reanalysis_precip_amt_kg_per_m2',
    'reanalysis_sat_precip_amt_mm',
    'dry_days'
]

# ✅ 4. Criar lags de 1 a 9 semanas por cidade
for col in cols_to_lag:
    for lag in [1,2,3,4,5,6,7,8,9]:
        df[f'{col}_lag{lag}'] = df.groupby('city')[col].shift(lag)
print(df)

# Lags e variáveis mais relevantes por cidade, com base na correlação
features_sj = [
    'reanalysis_dew_point_temp_k_lag6',
    'reanalysis_specific_humidity_g_per_kg_lag6',
    'station_avg_temp_c_lag6',
    'station_precip_mm_lag5',
    'precipitation_amt_mm_lag5',
    'dry_days_lag5',
]

features_iq = [
    'reanalysis_specific_humidity_g_per_kg_lag4',
    'reanalysis_dew_point_temp_k_lag4',
    'station_precip_mm_lag4',
    'precipitation_amt_mm_lag4',
    'dry_days_lag4',
]
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Carregar o dataset com lags

# Separar por cidade
df_sj = df[df['city'] == 'sj'].dropna(subset=features_sj + ['total_cases']).copy()
df_iq = df[df['city'] == 'iq'].dropna(subset=features_iq + ['total_cases']).copy()

# Função para treinar e avaliar o modelo
def train_and_evaluate(df, features, cidade):
    # Separar treino e teste (80% treino, 20% teste)
    split_index = int(len(df) * 0.8)
    X_train = df[features].iloc[:split_index]
    y_train = df['total_cases'].iloc[:split_index]
    X_test = df[features].iloc[split_index:]
    y_test = df['total_cases'].iloc[split_index:]

    # Modelo
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Avaliação
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae_norm = mae / y_test.mean()
    rmse_norm = rmse / y_test.mean()

    print(f"\n📊 {cidade.upper()}")
    print(f"MAE: {mae:.2f} (normalizado: {mae_norm:.3f})")
    print(f"RMSE: {rmse:.2f} (normalizado: {rmse_norm:.3f})")

    return y_test.reset_index(drop=True), pd.Series(y_pred)

# Aplicar
y_test_sj, y_pred_sj = train_and_evaluate(df_sj, features_sj, 'San Juan')
y_test_iq, y_pred_iq = train_and_evaluate(df_iq, features_iq, 'Iquitos')
