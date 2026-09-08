"""
Módulo de Auditoria Contratual de Fretes e Otimização Logística
===============================================================
Automatiza a conferência de Conhecimentos de Transporte Eletrônicos (CT-e)
cruzando dados faturados contra tabelas tarifárias contratuais vigentes.
"""

from datetime import datetime, timedelta
import numpy as np
import pandas as pd


def gerar_base_sintetica_ctes(n_registros: int = 800, seed: int = 42) -> pd.DataFrame:
    """Gera base simulada e calibrada de CT-es com divergências contratuais (14 transportadoras e R$ 1.2M em glosas)."""
    np.random.seed(seed)
    
    transportadoras = [
        "TRANS_ALPHA_LOG", "RAPIDO_COMETA", "CARGO_EXPRESS_BR", "RODO_VELOZ",
        "LOG_BRASIL_CARGA", "EXPRESSO_MERCURIO", "TRANSPAULO_FRETE", "RODOPRIME_LOG",
        "ATLAS_TRANSPORTES", "SOL_NASCENTE_CARGAS", "INTEGRA_LOG", "BRASIL_SUL_LOG",
        "NORTE_EXPRESS", "CONTINENTAL_CARGAS"
    ]
    cidades_destino = [
        "São Paulo - SP", "Rio de Janeiro - RJ", "Belo Horizonte - MG", "Curitiba - PR",
        "Porto Alegre - RS", "Salvador - BA", "Recife - PE", "Goiânia - GO",
        "Campinas - SP", "Joinville - SC"
    ]
    
    motivos_metas = {
        "Cubagem superestimada (peso volumétrico)": 540000.0,
        "Taxas acessórias indevidas (diárias/reentrega)": 384000.0,
        "Tarifa por kg cobrada acima do contrato": 192000.0,
        "Pedágio e GRIS calculados em duplicidade": 84000.0
    }
    contagens = {
        "Cubagem superestimada (peso volumétrico)": int(n_registros * 0.135),   # 108 em 800
        "Taxas acessórias indevidas (diárias/reentrega)": int(n_registros * 0.095), # 76 em 800
        "Tarifa por kg cobrada acima do contrato": int(n_registros * 0.0475),   # 38 em 800
        "Pedágio e GRIS calculados em duplicidade": int(n_registros * 0.0225)   # 18 em 800
    }

    n_glosas = sum(contagens.values())
    indices_glosa = np.random.choice(range(n_registros), size=n_glosas, replace=False)
    np.random.shuffle(indices_glosa)

    glosa_valores = np.zeros(n_registros)
    motivo_nomes = ["Conforme Contrato"] * n_registros

    cur = 0
    for mot, count in contagens.items():
        meta_val = motivos_metas[mot] * (n_registros / 800.0)
        sub_indices = indices_glosa[cur:cur + count]
        cur += count
        raw = np.random.uniform(0.6, 1.4, size=count)
        vals = np.round((raw / raw.sum()) * meta_val, 2)
        diff = round(meta_val - vals.sum(), 2)
        vals[0] += diff
        for idx, v in zip(sub_indices, vals):
            glosa_valores[idx] = round(float(v), 2)
            motivo_nomes[idx] = mot

    # Devido: soma calibrada para 6.920.000,00 (escala com n_registros)
    meta_devido = 6920000.0 * (n_registros / 800.0)
    raw_dev = np.random.uniform(4000.0, 14000.0, size=n_registros)
    devido_valores = np.round((raw_dev / raw_dev.sum()) * meta_devido, 2)
    diff_dev = round(meta_devido - devido_valores.sum(), 2)
    devido_valores[0] += diff_dev
    faturado_valores = np.round(devido_valores + glosa_valores, 2)

    registros = []
    data_inicio = pd.to_datetime("2025-01-10")

    for i in range(n_registros):
        transp = transportadoras[i % len(transportadoras)]
        dest = cidades_destino[i % len(cidades_destino)]
        dt = data_inicio + pd.Timedelta(days=int(i * (350 / n_registros)))
        peso_real = round(float(np.random.uniform(120.0, 3200.0)), 1)
        tem_glosa = glosa_valores[i] > 0
        if tem_glosa and "Cubagem" in motivo_nomes[i]:
            peso_cubado = round(peso_real * float(np.random.uniform(1.35, 1.85)), 1)
        else:
            peso_cubado = round(peso_real * float(np.random.uniform(0.70, 1.05)), 1)
            
        vol_m3 = round(peso_cubado / 300.0, 3)
        val_merc = round(float(devido_valores[i] * np.random.uniform(15.0, 35.0)), 2)
        
        registros.append({
            "numero_cte": f"CTE-{100000 + i + 1}",
            "transportadora": transp,
            "cidade_destino": dest,
            "data_emissao": dt.strftime("%Y-%m-%d"),
            "peso_real_kg": peso_real,
            "volume_m3": vol_m3,
            "peso_cubado_kg": peso_cubado,
            "peso_tarifado_esperado_kg": max(peso_real, peso_cubado),
            "valor_mercadoria": val_merc,
            "valor_devido": float(devido_valores[i]),
            "valor_faturado": float(faturado_valores[i]),
            "divergencia": float(glosa_valores[i]),
            "status_auditoria": "REJEITADO / GLOSA" if glosa_valores[i] > 10.0 else "APROVADO",
            "motivo_auditoria": motivo_nomes[i]
        })
        
    return pd.DataFrame(registros)


def recalcular_auditoria_dinamica(
    df: pd.DataFrame,
    fator_cubagem: float = 300.0,
    tolerancia_glosa: float = 10.0,
    aliquota_gris: float = 0.003
) -> pd.DataFrame:
    """Recalcula os valores devidos e status de auditoria com parâmetros dinâmicos."""
    df_recalc = df.copy()
    
    tarifas_base = {
        "TRANS_ALPHA_LOG": 28.50, "RAPIDO_COMETA": 32.00, "CARGO_EXPRESS_BR": 25.00, "RODO_VELOZ": 29.90,
        "LOG_BRASIL_CARGA": 31.00, "EXPRESSO_MERCURIO": 27.50, "TRANSPAULO_FRETE": 30.00, "RODOPRIME_LOG": 33.50,
        "ATLAS_TRANSPORTES": 26.00, "SOL_NASCENTE_CARGAS": 29.00, "INTEGRA_LOG": 28.00, "BRASIL_SUL_LOG": 32.50,
        "NORTE_EXPRESS": 35.00, "CONTINENTAL_CARGAS": 34.00
    }
    taxa_kg = {
        "TRANS_ALPHA_LOG": 0.85, "RAPIDO_COMETA": 0.95, "CARGO_EXPRESS_BR": 0.78, "RODO_VELOZ": 0.88,
        "LOG_BRASIL_CARGA": 0.89, "EXPRESSO_MERCURIO": 0.82, "TRANSPAULO_FRETE": 0.91, "RODOPRIME_LOG": 0.96,
        "ATLAS_TRANSPORTES": 0.80, "SOL_NASCENTE_CARGAS": 0.86, "INTEGRA_LOG": 0.84, "BRASIL_SUL_LOG": 0.93,
        "NORTE_EXPRESS": 1.05, "CONTINENTAL_CARGAS": 0.98
    }
    
    # Recalcula peso cubado e tarifado
    df_recalc["peso_cubado_kg"] = (df_recalc["volume_m3"] * fator_cubagem).round(2)
    df_recalc["peso_tarifado_esperado_kg"] = np.maximum(df_recalc["peso_real_kg"], df_recalc["peso_cubado_kg"]).round(2)
    
    # Recalcula tarifas
    def calc_devido(row):
        transp = row.get("transportadora", "TRANS_ALPHA_LOG")
        t_base = tarifas_base.get(transp, 28.50)
        t_kg = taxa_kg.get(transp, 0.85)
        peso = row["peso_tarifado_esperado_kg"]
        valor_merc = row.get("valor_mercadoria", 1000.0)
        
        pedagio = np.ceil(peso / 100.0) * 4.50
        ad_val = valor_merc * aliquota_gris
        return round(t_base + (t_kg * peso) + ad_val + pedagio, 2)
        
    df_recalc["valor_devido"] = df_recalc.apply(calc_devido, axis=1)
    df_recalc["divergencia"] = (df_recalc["valor_faturado"] - df_recalc["valor_devido"]).round(2)
    
    # Status com base na tolerância
    df_recalc["status_auditoria"] = np.where(
        df_recalc["divergencia"] > tolerancia_glosa,
        "REJEITADO / GLOSA",
        np.where(
            df_recalc["divergencia"] < -tolerancia_glosa,
            "REVISÃO MANUAL",
            "APROVADO"
        )
    )
    
    return df_recalc


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
    df = gerar_base_sintetica_ctes(800)
    kpis = executar_auditoria(df)
    
    print("\n--- RESULTADOS DA AUDITORIA EXECUTIVA ---")
    print(f"Total de CT-es Auditados: {kpis['total_ctes']}")
    print(f"CT-es com Divergências / Glosas: {kpis['ctes_glosados']} ({(kpis['ctes_glosados']/kpis['total_ctes'])*100:.1f}%)")
    print(f"Valor Total Faturado: R$ {kpis['total_faturado']:,.2f}")
    print(f"Valor Real Devido: R$ {kpis['total_devido']:,.2f}")
    print(f"Economia / Glosa Identificada: R$ {kpis['total_glosa_recuperavel']:,.2f} ({kpis['pct_glosa']}%)")
    print("\nDetalhamento por Transportadora:")
    print(kpis['resumo_transportadora'].to_string(index=False))
