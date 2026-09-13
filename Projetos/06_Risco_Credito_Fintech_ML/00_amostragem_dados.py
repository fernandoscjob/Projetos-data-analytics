import pandas as pd
import os

# Script de amostragem de dados para o Supabase
# Instruções: Coloque os arquivos originais baixados do Kaggle na pasta 'data/'

def criar_amostra():
    print("Lendo application_train.csv...")
    try:
        df_app = pd.read_csv('data/application_train.csv')
        
        # Amostra de 30 mil clientes
        df_app_sample = df_app.sample(n=30000, random_state=42)
        ids_escolhidos = df_app_sample['SK_ID_CURR'].tolist()
        
        # Salvar amostra
        df_app_sample.to_csv('data/app_amostra.csv', index=False)
        print("Amostra principal criada (app_amostra.csv)!")
        
        # Opcional: Processar tabela de histórico de empréstimos
        if os.path.exists('data/previous_application.csv'):
            print("Processando previous_application.csv...")
            df_prev = pd.read_csv('data/previous_application.csv')
            df_prev_sample = df_prev[df_prev['SK_ID_CURR'].isin(ids_escolhidos)]
            df_prev_sample.to_csv('data/prev_amostra.csv', index=False)
            print("Amostra de histórico criada (prev_amostra.csv)!")
            
    except FileNotFoundError:
        print("Arquivo não encontrado. Baixe do Kaggle e extraia os CSVs na pasta 'data/' primeiro.")

if __name__ == '__main__':
    criar_amostra()
