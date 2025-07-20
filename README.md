# 🦟 DengAI: Predição de Casos de Dengue

Projeto desenvolvido como parte do desafio **DengAI: Predicting Disease Spread**. O objetivo foi prever o número semanal de casos de dengue em duas cidades tropicais — **San Juan (Porto Rico)** e **Iquitos (Peru)** — utilizando dados climáticos, ambientais e temporais.

---

## 📁 Estrutura dos Dados

Fornecidos pela DrivenData, os dados incluem:

- **Características ambientais e climáticas** por semana
- **Número de casos registrados** por cidade
- Informações de NDVI (índice de vegetação), temperatura, precipitação, umidade e mais

As cidades analisadas são:
- 📍 **San Juan (sj)** — Hemisfério Norte
- 📍 **Iquitos (iq)** — Hemisfério Sul

---

## 🔍 Análise Exploratória

Inicialmente, foram inspecionadas as colunas, tipos de dados e valores ausentes. A seguir, iniciamos a exploração visual das variáveis por cidade.

### 🗓️ Sazonalidade
Identificamos estações seca e chuvosa para cada cidade:

- **San Juan:** estação chuvosa de maio a novembro  
- **Iquitos:** estação chuvosa de novembro a abril

<img width="845" height="556" alt="image" src="https://github.com/user-attachments/assets/1e7f10ef-b406-4b3c-915f-419e191b4b6a" />


---

## 🌿 Engenharia de Variáveis

### 🧪 Variáveis Criadas

- **NDVI médio**: média das quatro direções (NE, NW, SE, SW)
- **Dias secos**: dias com precipitação < 1mm
- **Defasagens (lags)**: de 1 a 9 semanas para todas as variáveis ambientais
- **Season**: uma variável para representar as estações do ano para cada cidade

<img width="1189" height="390" alt="image" src="https://github.com/user-attachments/assets/fbdb28c8-62a6-4f2d-928a-38faf126437f" />

<img width="1190" height="390" alt="image" src="https://github.com/user-attachments/assets/cb331baa-f8eb-45f7-a113-90158fdcd907" />


<img width="1389" height="390" alt="image" src="https://github.com/user-attachments/assets/9f38ffd6-bd9b-4bc8-a358-7ac898da02da" />

<img width="1389" height="390" alt="image" src="https://github.com/user-attachments/assets/23625845-74d9-4a64-80c0-f97a1099ecc9" />



<img width="757" height="628" alt="image" src="https://github.com/user-attachments/assets/fe815176-5eff-4987-b347-38763804432a" />

Fiz um gráfico como esse para cada variável proposta para o problema, para visualizar a correlação linear delas com o número de casos.


---

## 🧠 Modelagem

Foi utilizado o modelo **Random Forest Regressor**, com divisão temporal 80/20 para treino e teste. O modelo foi palicado separadamente para cada cidade.

### 🔧 Seleção de Variáveis

As variáveis foram escolhidas com base na correlação com `total_cases` e na interpretação climatológica. Algumas selecionadas:

#### 📍 San Juan

* `reanalysis_specific_humidity_g_per_kg_lag6`
* `reanalysis_dew_point_temp_k_lag6`
* `reanalysis_relative_humidity_percent_lag6`
* `station_avg_temp_c_lag6`
* `reanalysis_air_temp_k_lag6`
* `reanalysis_avg_temp_k_lag6`
* `dry_days` (sem defasagem)
* `season` (variável categórica)


#### 📍 Iquitos
* `reanalysis_specific_humidity_g_per_kg_lag6`
* `reanalysis_dew_point_temp_k_lag6`
* `reanalysis_air_temp_k_lag6`
* `reanalysis_avg_temp_k_lag6`
* `dry_days` (sem defasagem)
* `season` (variável categórica)


---

## 📊 Avaliação

| Cidade   | MAE   | MAE Normalizado | RMSE  | RMSE Normalizado |
|----------|-------|------------------|-------|-------------------|
| San Juan | 21.02 | 0.831            | 28.74 | 1.137             |
| Iquitos  | 7.88  | 0.909            | 11.61 | 1.338             |

<img width="1189" height="390" alt="image" src="https://github.com/user-attachments/assets/da586d51-2b0c-4dce-b070-5b482880da0a" />
  
<img width="1189" height="390" alt="image" src="https://github.com/user-attachments/assets/fc45e9b6-32d0-4d21-a843-1a95e0a24c2c" />


---

## 🧭 Considerações Finais

- Iquitos apresentou melhores resultados com menos variabilidade de casos
- O uso de lags permitiu capturar dinâmicas epidemiológicas relevantes
- A combinação de temperatura e umidade foi particularmente significativa em ambas as cidades
- O modelo ainda apresenta potencial de melhoria, especialmente em San Juan

---

## 📌 Possíveis Extensões

- Testar outros modelos (LSTM, XGBoost)
- Modelar separadamente para cada cidade
- Incluir mais dados externos (mobilidade, campanhas públicas etc.)

---

## 📎 Referência

> Este projeto foi desenvolvido no contexto do [Desafio DengAI](https://www.drivendata.org/competitions/44/dengai-predicting-disease-spread/), utilizando Python, pandas, seaborn e scikit-learn.
