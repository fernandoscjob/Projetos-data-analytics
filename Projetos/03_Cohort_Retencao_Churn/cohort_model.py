"""
Modelagem de Cohort, Retenção Longitudinal & Prevenção de Churn
==============================================================
Processa histórico de transações/assinaturas de clientes para construir a matriz
de retenção por safras (First-Touch Cohort) de M0 a M6+, identificando gargalos
de Early Churn e queda de engajamento nos primeiros 60 dias.
"""

from datetime import datetime, timedelta
import numpy as np
import pandas as pd


def gerar_base_sintetica_transacoes(n_clientes: int = 400, seed: int = 42) -> pd.DataFrame:
    """Gera transações recorrentes com curva realista de retenção e churn precoce."""
    np.random.seed(seed)
    
    safras = pd.date_range(start="2025-01-01", periods=6, freq="MS")
    registros = []
    
    for i in range(1, n_clientes + 1):
        cliente_id = f"CLI-COH-{1000 + i}"
        safra = pd.to_datetime(np.random.choice(safras))
        
        # O cliente faz compras em M0 garantido (mês de entrada)
        registros.append({
            "cliente_id": cliente_id,
            "data_transacao": safra + timedelta(days=int(np.random.uniform(1, 20))),
            "valor": round(float(np.random.uniform(80.0, 450.0)), 2),
            "safra_mes": safra.strftime("%Y-%m")
        })
        
        # Probabilidades de retenção decrescentes simulando SaaS / E-commerce recorrente
        # M1 (D30): 75%, M2 (D60): 58%, M3 (D90): 48%, M4 (D120): 43%, M5 (D150): 40%
        prob_retencao = [0.75, 0.58, 0.48, 0.43, 0.40]
        
        for m_idx, prob in enumerate(prob_retencao, start=1):
            data_m = safra + pd.DateOffset(months=m_idx)
            if data_m > datetime(2025, 8, 1):
                break
                
            # Se o cliente continuar ativo
            if np.random.rand() < prob:
                registros.append({
                    "cliente_id": cliente_id,
                    "data_transacao": data_m + timedelta(days=int(np.random.uniform(1, 25))),
                    "valor": round(float(np.random.uniform(70.0, 420.0)), 2),
                    "safra_mes": safra.strftime("%Y-%m")
                })
            else:
                # Evasão (Churn) - cliente para de comprar
                break
                
    return pd.DataFrame(registros)


def calcular_matriz_cohort(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Calcula tamanho de safras, retenção absoluta e taxa percentual de retenção/churn."""
    df["mes_transacao"] = pd.to_datetime(df["data_transacao"]).dt.to_period("M")
    df["safra_period"] = pd.to_datetime(df["safra_mes"]).dt.to_period("M")
    
    # Período relativo (M0, M1, M2...)
    df["periodo_m"] = (df["mes_transacao"].dt.year - df["safra_period"].dt.year) * 12 + (df["mes_transacao"].dt.month - df["safra_period"].dt.month)
    
    # Tabela dinâmica de contagem única de clientes
    cohort_counts = df.groupby(["safra_mes", "periodo_m"])["cliente_id"].nunique().unstack(fill_value=0)
    
    # Tamanho da safra (M0)
    tamanho_safras = cohort_counts[0]
    
    # Matriz percentual de retenção
    cohort_retention_pct = cohort_counts.divide(tamanho_safras, axis=0) * 100.0
    
    # Matriz percentual de Churn acumulado
    cohort_churn_pct = 100.0 - cohort_retention_pct
    
    return cohort_counts, cohort_retention_pct.round(1), cohort_churn_pct.round(1)


if __name__ == "__main__":
    print("Gerando dados sintéticos para modelagem de safras...")
    df = gerar_base_sintetica_transacoes(500)
    contagens, retencao, churn = calcular_matriz_cohort(df)
    
    print("\n--- MATRIZ DE RETENÇÃO (%) POR SAFRA (COHORT RETENTION) ---")
    print(retencao.fillna("-").to_string())
    
    print("\n--- MATRIZ DE CHURN (%) ACUMULADO ---")
    print(churn.fillna("-").to_string())
    
    media_m1 = retencao[1].dropna().mean()
    media_m3 = retencao[3].dropna().mean()
    print(f"\nRetenção Média M1 (30 dias): {media_m1:.1f}% (Early Churn de {100 - media_m1:.1f}%)")
    print(f"Retenção Média M3 (90 dias): {media_m3:.1f}%")
