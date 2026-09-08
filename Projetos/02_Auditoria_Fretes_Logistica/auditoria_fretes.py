"""
Módulo de Auditoria Contratual de Fretes e Otimização Logística
===============================================================
Automatiza a conferência de Conhecimentos de Transporte Eletrônicos (CT-e)
cruzando dados faturados contra tabelas tarifárias contratuais vigentes.
"""

from datetime import datetime, timedelta
import numpy as np
import pandas as pd


def gerar_base_sintetica_ctes(n_registros: int = 500, seed: int = 42) -> pd.DataFrame:
    """Gera base simulada realista de CT-es com divergências contratuais."""
    np.random.seed(seed)
    
    transportadoras = ["TRANS_ALPHA_LOG", "RAPIDO_COMETA", "CARGO_EXPRESS_BR", "RODO_VELOZ"]
    cidades_destino = ["São Paulo - SP", "Rio de Janeiro - RJ", "Belo Horizonte - MG", "Curitiba - PR", "Porto Alegre - RS", "Salvador - BA"]
    
    registros = []
    data_base = datetime.now() - timedelta(days=90)
    
    for i in range(1, n_registros + 1):
        cte_id = f"CTE-{100000 + i}"
        transp = np.random.choice(transportadoras)
        destino = np.random.choice(cidades_destino)
        data_emissao = data_base + timedelta(days=int(np.random.uniform(0, 90)))
        
        # Parâmetros físicos
        peso_real = round(float(np.random.exponential(scale=35.0) + 2.0), 2)
        volume_m3 = round(float(np.random.uniform(0.02, 0.45)), 3)
        valor_mercadoria = round(float(np.random.uniform(150.0, 4500.0)), 2)
        
        # Fator de cubagem contratual padrão: 300 kg/m³
        fator_cubagem = 300.0
        peso_cubado = volume_m3 * fator_cubagem
        peso_tarifado_esperado = max(peso_real, peso_cubado)
        
        # Tarifa base contratual por transportadora
        tarifas_base = {"TRANS_ALPHA_LOG": 28.50, "RAPIDO_COMETA": 32.00, "CARGO_EXPRESS_BR": 25.00, "RODO_VELOZ": 29.90}
        taxa_kg = {"TRANS_ALPHA_LOG": 0.85, "RAPIDO_COMETA": 0.95, "CARGO_EXPRESS_BR": 0.78, "RODO_VELOZ": 0.88}
        
        tarifa_fixa = tarifas_base[transp]
        tarifa_peso = taxa_kg[transp] * peso_tarifado_esperado
        ad_valorem = valor_mercadoria * 0.003  # 0.3% GRIS / seguro
        pedagio = np.ceil(peso_tarifado_esperado / 100.0) * 4.50
        
        valor_devido_calculado = round(tarifa_fixa + tarifa_peso + ad_valorem + pedagio, 2)
        
        # Simulação de erros operacionais e sobretaxas indevidas em ~25% das faturas
        tem_divergencia = np.random.rand() < 0.25
        if tem_divergencia:
            tipo_erro = np.random.choice(["cubagem_superestimada", "taxa_reentrega_indevida", "tarifa_fora_contrato"])
            if tipo_erro == "cubagem_superestimada":
                valor_faturado = valor_devido_calculado + round(float(np.random.uniform(25.0, 95.0)), 2)
                motivo = "Cubagem aferida superior à real"
            elif tipo_erro == "taxa_reentrega_indevida":
                valor_faturado = valor_devido_calculado + 45.00
                motivo = "Taxa de reentrega cobrada sem comprovação"
            else:
                valor_faturado = round(valor_devido_calculado * 1.18, 2)
                motivo = "Tarifa por kg cobrada acima do contrato"
        else:
            valor_faturado = valor_devido_calculado
            motivo = "Conforme Contrato"
            
        registros.append({
            "numero_cte": cte_id,
            "transportadora": transp,
            "cidade_destino": destino,
            "data_emissao": data_emissao.strftime("%Y-%m-%d"),
            "peso_real_kg": peso_real,
            "volume_m3": volume_m3,
            "peso_cubado_kg": round(peso_cubado, 2),
            "peso_tarifado_esperado_kg": round(peso_tarifado_esperado, 2),
            "valor_mercadoria": valor_mercadoria,
            "valor_devido": valor_devido_calculado,
            "valor_faturado": valor_faturado,
            "divergencia": round(valor_faturado - valor_devido_calculado, 2),
            "status_auditoria": "REJEITADO / GLOSA" if valor_faturado - valor_devido_calculado > 5.0 else "APROVADO",
            "motivo_auditoria": motivo
        })
        
    return pd.DataFrame(registros)


def executar_auditoria(df: pd.DataFrame) -> dict:
    """Calcula KPIs consolidados de auditoria e glosas."""
    total_faturado = df["valor_faturado"].sum()
    total_devido = df["valor_devido"].sum()
    total_glosa = df.loc[df["divergencia"] > 0, "divergencia"].sum()
    pct_glosa = (total_glosa / total_faturado) * 100.0 if total_faturado > 0 else 0
    
    total_ctes = len(df)
    ctes_glosados = len(df[df["divergencia"] > 5.0])
    
    resumo_transp = df.groupby("transportadora").agg(
        total_ctes=("numero_cte", "count"),
        total_faturado=("valor_faturado", "sum"),
        total_devido=("valor_devido", "sum"),
        total_glosa=("divergencia", lambda x: x[x > 0].sum())
    ).reset_index()
    resumo_transp["pct_divergencia"] = (resumo_transp["total_glosa"] / resumo_transp["total_faturado"]) * 100
    
    return {
        "total_ctes": total_ctes,
        "ctes_glosados": ctes_glosados,
        "total_faturado": round(total_faturado, 2),
        "total_devido": round(total_devido, 2),
        "total_glosa_recuperavel": round(total_glosa, 2),
        "pct_glosa": round(pct_glosa, 2),
        "resumo_transportadora": resumo_transp
    }


if __name__ == "__main__":
    print("Iniciando simulação e auditoria contratual de fretes...")
    df = gerar_base_sintetica_ctes(500)
    kpis = executar_auditoria(df)
    
    print("\n--- RESULTADOS DA AUDITORIA EXECUTIVA ---")
    print(f"Total de CT-es Auditados: {kpis['total_ctes']}")
    print(f"CT-es com Divergências / Glosas: {kpis['ctes_glosados']} ({(kpis['ctes_glosados']/kpis['total_ctes'])*100:.1f}%)")
    print(f"Valor Total Faturado: R$ {kpis['total_faturado']:,.2f}")
    print(f"Valor Real Devido: R$ {kpis['total_devido']:,.2f}")
    print(f"Economia / Glosa Identificada: R$ {kpis['total_glosa_recuperavel']:,.2f} ({kpis['pct_glosa']}%)")
    print("\nDetalhamento por Transportadora:")
    print(kpis['resumo_transportadora'].to_string(index=False))
