import os
import pandas as pd
from google.cloud import bigquery
from dotenv import load_dotenv

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import roc_auc_score, classification_report
import xgboost as xgb
import joblib

# Carrega variáveis
load_dotenv()

def treinar_modelo_tunado():
    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        print("GCP_PROJECT_ID não encontrado no .env")
        return

    print("Baixando dados do BigQuery (dim_clientes_credito)...")
    bq_client = bigquery.Client(project=project_id)
    query = f"SELECT * FROM `{project_id}.analytics_dev.dim_clientes_credito`"
    df = bq_client.query(query).to_dataframe()
    
    # O alvo é a coluna TARGET.
    X = df.drop(columns=['TARGET', 'SK_ID_CURR'])
    y = df['TARGET']

    # Separação Treino e Teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Lidando com o Desbalanceamento: Calculando a proporção de Bons / Maus pagadores
    # scale_pos_weight = sum(negative instances) / sum(positive instances)
    bons_pagadores = y_train.value_counts()[0]
    maus_pagadores = y_train.value_counts()[1]
    peso_desbalanceamento = bons_pagadores / maus_pagadores

    print(f"Desbalanceamento detectado. Aplicando peso de {peso_desbalanceamento:.2f} para a classe minoritária...")

    num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    cat_cols = X.select_dtypes(include=['object', 'string']).columns.tolist()

    # Pipelines de pré-processamento
    num_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    cat_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_transformer, num_cols),
            ('cat', cat_transformer, cat_cols)
        ])

    print("Criando o modelo XGBoost Tunado...")
    # Ajustamos alguns hiperparâmetros para evitar Overfitting e lidar com a minoria
    xgb_model = xgb.XGBClassifier(
        n_estimators=200,             # Mais árvores
        learning_rate=0.05,           # Aprendizado mais lento e consistente
        max_depth=5,                  # Árvores um pouco mais fundas
        subsample=0.8,                # Usa 80% das linhas por árvore (evita overfit)
        colsample_bytree=0.8,         # Usa 80% das colunas por árvore
        scale_pos_weight=peso_desbalanceamento, # A mágica para o desbalanceamento!
        random_state=42,
        eval_metric='auc'
    )

    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', xgb_model)
    ])

    print("Treinando o modelo...")
    model_pipeline.fit(X_train, y_train)

    print("\nTreinamento concluído! Avaliando...")
    y_pred_proba = model_pipeline.predict_proba(X_test)[:, 1]
    y_pred = model_pipeline.predict(X_test)

    auc = roc_auc_score(y_test, y_pred_proba)
    print(f"\n[SUCESSO] NOVO ROC-AUC Score: {auc:.4f}")
    
    print("\nRelatório de Classificação Melhorado:")
    print(classification_report(y_test, y_pred))

    # Vamos salvar o modelo para podermos usar no Dashboard depois!
    caminho_modelo = "03_machine_learning/modelo_risco_credito.pkl"
    joblib.dump(model_pipeline, caminho_modelo)
    print(f"\nModelo salvo com sucesso em: {caminho_modelo}. Pronto para o Dashboard!")

if __name__ == "__main__":
    treinar_modelo_tunado()
