import os
import pandas as pd
from sqlalchemy import create_engine
from google.cloud import bigquery
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

def supabase_to_bigquery():
    # Credenciais do Supabase
    db_url = os.getenv("SUPABASE_DB_URL")
    if not db_url:
        print("Erro: SUPABASE_DB_URL não encontrada no .env")
        return

    # Credenciais do GCP (BigQuery)
    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        print("Erro: GCP_PROJECT_ID não encontrada no .env")
        return

    print("Conectando ao Supabase e ao BigQuery...")
    # Engine do Postgres
    engine = create_engine(db_url)
    
    # Cliente do BigQuery (usará automaticamente o GOOGLE_APPLICATION_CREDENTIALS do .env)
    bq_client = bigquery.Client(project=project_id)

    # Dataset no BigQuery onde os dados brutos vão ficar
    dataset_id = f"{project_id}.raw_data"

    # Cria o dataset no BQ caso não exista
    print(f"Garantindo que o dataset '{dataset_id}' existe no BigQuery...")
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "US"
    bq_client.create_dataset(dataset, exists_ok=True)

    tabelas = ['applications', 'previous_applications']

    for table in tabelas:
        print(f"\nExtraindo '{table}' do Supabase...")
        query = f"SELECT * FROM {table}"
        
        # Lê do Supabase para um DataFrame
        df = pd.read_sql(query, engine)
        print(f"{len(df)} linhas extraídas.")

        # O BigQuery não aceita nomes de coluna com espaços ou caracteres muito estranhos. 
        # Nossos CSVs originais geralmente já vêm limpos, mas é bom formatar se necessário.
        df.columns = df.columns.str.replace(' ', '_').str.replace('-', '_')

        table_id = f"{dataset_id}.{table}"
        
        print(f"Carregando dados na tabela '{table_id}' no BigQuery...")
        
        # Configuração do Job de upload
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE", # Substitui a tabela se já existir
        )

        job = bq_client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()  # Aguarda o término

        print(f"Tabela '{table}' carregada com sucesso no BigQuery!")

if __name__ == "__main__":
    supabase_to_bigquery()
