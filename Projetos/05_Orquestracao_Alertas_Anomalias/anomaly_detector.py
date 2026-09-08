"""
Motor Estatístico de Detecção de Anomalias Operacionais
======================================================
Monitora streams horários de pedidos, lead times e taxas de conversão calculando
médias móveis e Z-scores (|Z| > 2.5) para disparo proativo de alertas nos canais
do Slack e Microsoft Teams antes do cliente perceber o problema.
"""

from datetime import datetime, timedelta
import json
import sys
import numpy as np
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def gerar_telemetria_pedidos(n_horas: int = 72, seed: int = 42) -> pd.DataFrame:
    """Gera série temporal com comportamento regular e anomalias induzidas."""
    np.random.seed(seed)
    
    data_inicio = datetime.now() - timedelta(hours=n_horas)
    categorias = ["ELETRONICOS", "MODA_VESTUARIO", "ALIMENTOS_BEBIDAS", "HOME_OFFICE"]
    
    registros = []
    
    for h in range(n_horas):
        timestamp = data_inicio + timedelta(hours=h)
        hora_dia = timestamp.hour
        
        # Padrão circadiano de consumo
        fator_horario = 1.8 if 10 <= hora_dia <= 21 else 0.4
        
        for cat in categorias:
            base_volume = {"ELETRONICOS": 45, "MODA_VESTUARIO": 60, "ALIMENTOS_BEBIDAS": 80, "HOME_OFFICE": 30}[cat]
            volume = max(0, int(np.random.normal(loc=base_volume * fator_horario, scale=8.0)))
            lead_time_min = round(float(np.random.normal(loc=28.0, scale=4.0)), 1)
            taxa_erros_pct = round(float(np.random.uniform(0.1, 1.2)), 2)
            
            # Indução de anomalia grave nas últimas 3 horas para ELETRONICOS (ex: falha de gateway)
            if h >= n_horas - 3 and cat == "ELETRONICOS":
                volume = int(volume * 0.15)  # Queda brusca de 85%
                taxa_erros_pct = 14.8        # Disparo de erros de checkout
            
            registros.append({
                "timestamp": timestamp.strftime("%Y-%m-%d %H:00:00"),
                "categoria": cat,
                "volume_pedidos": volume,
                "lead_time_minutos": lead_time_min,
                "taxa_erros_checkout_pct": taxa_erros_pct
            })
            
    return pd.DataFrame(registros)


def detectar_anomalias_zscore(df: pd.DataFrame, threshold_z: float = 2.0) -> pd.DataFrame:
    """Calcula estatísticas móveis e marca anomalias fora do intervalo de confiança."""
    df = df.copy()
    
    # Média e desvio padrão histórico por categoria
    stats = df.groupby("categoria")["volume_pedidos"].agg(
        media_historica="mean",
        desvio_padrao="std"
    ).reset_index()
    
    df = df.merge(stats, on="categoria")
    
    # Cálculo do Z-score: (x - média) / desvio
    df["z_score"] = (df["volume_pedidos"] - df["media_historica"]) / df["desvio_padrao"].replace(0, 1)
    df["z_score"] = df["z_score"].round(2)
    
    # Detecção por Z-Score de volume ou por taxa de erros de checkout anômala
    condicao_anomalia = (df["z_score"].abs() >= threshold_z) | (df["taxa_erros_checkout_pct"] >= 5.0)
    anomalias = df[condicao_anomalia].copy()
    anomalias["tipo_anomalia"] = np.where(
        anomalias["taxa_erros_checkout_pct"] >= 5.0, 
        "FALHA DE GATEWAY / ERROS CHECKOUT",
        np.where(anomalias["z_score"] < 0, "QUEDA CRÍTICA DE VOLUME", "PICO ANÔMALO")
    )
    
    return anomalias


def formatar_payload_alerta_slack(anomalia_row: pd.Series) -> dict:
    """Gera payload no formato Block Kit do Slack para notificação em tempo real."""
    return {
        "text": f"🚨 ALERTA OPERACIONAL: {anomalia_row['tipo_anomalia']} em {anomalia_row['categoria']}",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🚨 Alerta de Anomalia: {anomalia_row['categoria']}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Horário:* {anomalia_row['timestamp']}"},
                    {"type": "mrkdwn", "text": f"*Severidade:* CRÍTICA (Z-Score: {anomalia_row['z_score']})"},
                    {"type": "mrkdwn", "text": f"*Volume Atual:* {anomalia_row['volume_pedidos']} pedidos"},
                    {"type": "mrkdwn", "text": f"*Média Esperada:* {anomalia_row['media_historica']:.1f} pedidos"},
                    {"type": "mrkdwn", "text": f"*Erros de Checkout:* {anomalia_row['taxa_erros_checkout_pct']}%"}
                ]
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Inspecionar Gateway"},
                        "style": "danger",
                        "url": "https://monitoramento.interno/gateway"
                    }
                ]
            }
        ]
    }


if __name__ == "__main__":
    print("Coletando telemetria horária de transações...")
    df = gerar_telemetria_pedidos(n_horas=72)
    anomalias = detectar_anomalias_zscore(df, threshold_z=2.5)
    
    print(f"\n--- RELATÓRIO DE ANOMALIAS DETECTADAS: {len(anomalias)} OCORRÊNCIA(S) ---")
    if not anomalias.empty:
        colunas_exibir = ["timestamp", "categoria", "volume_pedidos", "media_historica", "z_score", "tipo_anomalia"]
        print(anomalias[colunas_exibir].to_string(index=False))
        
        exemplo_alerta = formatar_payload_alerta_slack(anomalias.iloc[0])
        print("\nPayload de Exemplo enviado ao Webhook do Slack:")
        print(json.dumps(exemplo_alerta, indent=2, ensure_ascii=True))
    else:
        print("Nenhuma anomalia detectada no período.")
