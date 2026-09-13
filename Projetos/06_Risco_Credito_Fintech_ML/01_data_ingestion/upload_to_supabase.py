import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (ex: string de conexão do Supabase)
load_dotenv()

def upload_to_supabase():
    # A string de conexão do PostgreSQL fornecida pelo Supabase
    # Exemplo: postgresql://postgres.[project-ref]:[password]@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
    db_url = os.getenv("SUPABASE_DB_URL")
    
    if not db_url:
        print("Erro: Variável de ambiente SUPABASE_DB_URL não encontrada.")
        print("Crie um arquivo .env na raiz do projeto com esta variável.")
        return

    print("Conectando ao banco de dados Supabase...")
    engine = create_engine(db_url)

    # Dicionário mapeando o arquivo CSV para o nome da tabela no banco
    tabelas = {
        'data/app_amostra.csv': 'applications',
        'data/prev_amostra.csv': 'previous_applications'
    }

    for csv_file, table_name in tabelas.items():
        if os.path.exists(csv_file):
            print(f"Lendo {csv_file}...")
            df = pd.read_csv(csv_file)
            
            print(f"Enviando dados para a tabela '{table_name}' no Supabase...")
            # to_sql cria a tabela automaticamente se não existir
            df.to_sql(table_name, engine, if_exists='replace', index=False, chunksize=5000)
            print(f"Tabela '{table_name}' criada/atualizada com sucesso!")
        else:
            print(f"Aviso: Arquivo {csv_file} não encontrado. Execute o script de amostragem primeiro.")

if __name__ == "__main__":
    upload_to_supabase()
