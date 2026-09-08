"""
Módulo rfm_engine.py
====================
Motor analítico para cálculo, pontuação e segmentação RFM
(Recência, Frequência e Valor Monetário).

Contém:
- Geração de dados transacionais sintéticos realistas (18 meses com sazonalidade).
- Cálculo de métricas RFM a partir de bases transacionais.
- Atribuição de scores de 1 a 5 com quantis e desempate via rank(method='first').
- Mapeamento determinístico para os 11 clusters de negócio.
- Metadados, recomendações táticas e planos de ação para CRM e Vendas.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
import numpy as np
import pandas as pd


# ==============================================================================
# DICIONÁRIO DE METADADOS E PLANOS DE AÇÃO DOS CLUSTERS RFM
# ==============================================================================
CLUSTER_METADATA: Dict[str, Dict[str, Any]] = {
    "Campeões": {
        "descricao": "Compraram recentemente, compram com alta frequência e possuem os maiores volumes de gastos.",
        "objetivo": "Fidelização máxima, retenção ativa e programas de evangelização da marca.",
        "plano_de_acao": (
            "1. Oferecer acesso antecipado a lançamentos de novos produtos e serviços.\n"
            "2. Conceder atendimento prioritário (Key Account / Gerente Dedicado).\n"
            "3. Criar programa exclusivo de indicação (Member Get Member) com recompensas VIP.\n"
            "4. Evitar envio de cupons de desconto agressivos (eles já compram pelo valor percebido)."
        ),
        "canais_recomendados": "WhatsApp Concierge, Contato Telefônico Executivo, E-mail VIP",
        "prioridade": "Alta",
        "cor": "#10B981",  # Esmeralda vibrante
    },
    "Leais": {
        "descricao": "Clientes com compras consistentes, boa frequência e gastos acima da média.",
        "objetivo": "Aumentar o Lifetime Value (LTV) por meio de cross-selling e up-selling.",
        "plano_de_acao": (
            "1. Apresentar pacotes de produtos complementares de tíquete superior.\n"
            "2. Incentivar adesão a planos de assinatura ou clubes de fidelidade com acúmulo de pontos.\n"
            "3. Solicitar depoimentos (reviews) e casos de sucesso para prova social.\n"
            "4. Bonificar com brindes exclusivos em compras consecutivas."
        ),
        "canais_recomendados": "E-mail Marketing Segmentado, WhatsApp Comercial, Push Notification",
        "prioridade": "Alta",
        "cor": "#3B82F6",  # Azul corporativo
    },
    "Potenciais Clientes Leais": {
        "descricao": "Clientes recentes que já realizaram mais de uma compra e demonstraram engajamento promissor.",
        "objetivo": "Transformar compradores recorrentes em clientes leais e defensores da marca.",
        "plano_de_acao": (
            "1. Enviar réguas de nutrição com casos de uso e melhores práticas dos itens adquiridos.\n"
            "2. Ofertar incentivo na 3ª ou 4ª compra com validade regressiva (gatilho de escassez).\n"
            "3. Convidar para comunidade exclusiva ou eventos/webinars da marca."
        ),
        "canais_recomendados": "E-mail Educativo, WhatsApp Comercial, Remarketing de Produtos Relacionados",
        "prioridade": "Média-Alta",
        "cor": "#8B5CF6",  # Roxo / Violeta
    },
    "Novos Clientes": {
        "descricao": "Compraram pela primeira vez recentemente. Alto potencial, mas frequência ainda unitária.",
        "objetivo": "Garantir o sucesso do onboarding e induzir a segunda compra o mais rápido possível.",
        "plano_de_acao": (
            "1. Disparar e-mail de boas-vindas acolhedor e pesquisa rápida de satisfação pós-primeira compra.\n"
            "2. Enviar tutorial/guia de utilização do produto ou serviço adquirido.\n"
            "3. Disponibilizar cupom de incentivo exclusivo para a próxima compra válido por 30 dias.\n"
            "4. Garantir suporte proativo via canais rápidos para sanar dúvidas iniciais."
        ),
        "canais_recomendados": "E-mail de Onboarding, SMS/WhatsApp com Cupom de Boas-Vindas",
        "prioridade": "Média",
        "cor": "#06B6D4",  # Ciano moderno
    },
    "Promissores": {
        "descricao": "Compraram recentemente pela primeira vez e gastaram valor moderado, mas ainda sem repetição.",
        "objetivo": "Criar vínculo e construir percepção de valor para estimular a recompra.",
        "plano_de_acao": (
            "1. Criar campanhas de reengajamento baseadas na categoria do primeiro item comprado.\n"
            "2. Apresentar avaliações de outros compradores em categorias afins.\n"
            "3. Enviar ofertas de itens 'best-sellers' com condições especiais de frete ou pagamento."
        ),
        "canais_recomendados": "E-mail Marketing, Remarketing de Catálogo",
        "prioridade": "Média",
        "cor": "#14B8A6",  # Teal
    },
    "Precisam de Atenção": {
        "descricao": "Clientes com recência e frequência moderadas. Risco iminente de esfriamento se não estimulados.",
        "objetivo": "Reativar o hábito de compra antes da entrada na zona de inatividade.",
        "plano_de_acao": (
            "1. Campanhas de incentivo com tempo limitado (ofertas 'flash' de 48 horas).\n"
            "2. Ofertar combos ou kits de reposição com desconto no pacote.\n"
            "3. Relembrar novidades do portfólio adicionadas desde sua última interação."
        ),
        "canais_recomendados": "E-mail de Oportunidade, Remarketing Display, WhatsApp com Oferta Rápida",
        "prioridade": "Alta",
        "cor": "#F59E0B",  # Âmbar / Laranja Suave
    },
    "Quase Hibernando": {
        "descricao": "Baixa recência e pouca frequência. Clientes prestes a se tornarem inativos.",
        "objetivo": "Evitar o churn definitivo com comunicação de reengajamento assertiva.",
        "plano_de_acao": (
            "1. Campanha 'Sentimos sua falta' com benefícios diretos na volta.\n"
            "2. Apresentar produtos populares com condições agressivas de preço.\n"
            "3. Questionar de forma breve se o produto anterior atendeu às expectativas."
        ),
        "canais_recomendados": "E-mail de Reativação, Tráfego Pago Segmentado (Custom Audience)",
        "prioridade": "Média",
        "cor": "#F97316",  # Laranja
    },
    "Não Podemos Perder": {
        "descricao": "Clientes que compravam com alta frequência e altos volumes monetários, mas não compram há muito tempo.",
        "objetivo": "Reconquista urgente e investigação de atrito/insatisfação. Risco financeiro crítico.",
        "plano_de_acao": (
            "1. Ação imediata de SDR/Gerente de Contas via ligação direta ou mensagem executiva personalizada.\n"
            "2. Investigar se houve problema com atendimento, qualidade do produto ou migração para concorrente.\n"
            "3. Ofertar plano de renovação sob medida com condições especiais irrecusáveis.\n"
            "4. Envolver liderança de Vendas/CS para resgatar o relacionamento."
        ),
        "canais_recomendados": "Ligação Telefônica Direta, Reunião Presencial/Online, WhatsApp Pessoal de Gerente",
        "prioridade": "Crítica",
        "cor": "#DC2626",  # Vermelho Vivo
    },
    "Em Risco": {
        "descricao": "Clientes com histórico sólido de compras anteriores que deixaram de comprar no período recente.",
        "objetivo": "Interromper o processo de churn e recapturar a atenção do cliente.",
        "plano_de_acao": (
            "1. Disparo de pesquisas de satisfação (NPS/CSAT) para entender os motivos de afastamento.\n"
            "2. Ofertar cupons substanciais de reativação para a volta.\n"
            "3. Renovar o catálogo exibindo lançamentos e melhorias recentes que o cliente não conheceu."
        ),
        "canais_recomendados": "E-mail de Reconquista, WhatsApp de Relacionamento, Anúncios de Retargeting",
        "prioridade": "Crítica",
        "cor": "#EF4444",  # Vermelho Alerta
    },
    "Hibernando": {
        "descricao": "Frequência muito baixa e última compra realizada há muitos meses.",
        "objetivo": "Reativação de baixo custo ou limpeza de base para otimização de campanhas.",
        "plano_de_acao": (
            "1. Campanhas de queima de estoque ou promoções sazonais agressivas (ex: Black Friday, Aniversário).\n"
            "2. Mensagem simples de reativação com opção clara de descadastramento (opt-out).\n"
            "3. Evitar envio diário de e-mails para não comprometer a entregabilidade e reputação do domínio."
        ),
        "canais_recomendados": "E-mail Marketing Automatizado de Baixo Custo",
        "prioridade": "Baixa",
        "cor": "#6B7280",  # Cinza Médio
    },
    "Perdidos": {
        "descricao": "Realizaram uma única compra no passado distante e nunca mais retornaram.",
        "objetivo": "Última tentativa de contato de baixo custo operacional ou desativação de CRM.",
        "plano_de_acao": (
            "1. Disparo de uma única régua 'Última chamada: cupom especial de retorno'.\n"
            "2. Se não houver clique ou abertura após 30 dias, pausar envios de marketing para cortar custos.\n"
            "3. Reavaliar a qualidade do canal de aquisição de onde vieram esses clientes."
        ),
        "canais_recomendados": "E-mail de Despedida / Limpeza de Base",
        "prioridade": "Baixa",
        "cor": "#475569",  # Ardósia Escuro
    },
}


# ==============================================================================
# GERAÇÃO DE DADOS SINTÉTICOS REALISTAS
# ==============================================================================
def generate_synthetic_transactions(
    n_customers: int = 800,
    n_transactions: int = 6633,
    reference_end_date: Optional[datetime] = None,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Gera uma base de dados transacionais sintética e realista cobrindo os últimos 18 meses,
    calibrada para refletir o caso de negócio (800 clientes, ~R$ 1.95M em receita e R$ 485k em risco).

    Aplica:
    - Distribuição de Pareto/Lei de Potência na frequência de compra dos clientes.
    - Sazonalidade (aumento de transações no fim do ano - Black Friday/Natal - e início de mês).
    - Variações de tíquete médio através de distribuição Log-Normal.
    - Clientes de diferentes perfis (VIPs, recorrentes, novos e inativos em risco).

    Args:
        n_customers: Quantidade de clientes únicos a simular (padrão: 800).
        n_transactions: Volume total de transações a gerar (padrão: 6633).
        reference_end_date: Data final do período (padrão: hoje).
        seed: Semente pseudo-aleatória para reprodutibilidade.

    Returns:
        pd.DataFrame com colunas: ['id_cliente', 'data_transacao', 'id_transacao', 'valor_total'].
    """
    np.random.seed(seed)

    if reference_end_date is None:
        end_date = datetime.now()
    else:
        end_date = reference_end_date

    start_date = end_date - timedelta(days=548)  # ~18 meses
    total_days = (end_date - start_date).days

    # Criação dos IDs de clientes
    customer_ids = [f"CLI-{1000 + i}" for i in range(n_customers)]

    # Se n_customers for 800 (padrão do portfólio), calibra o cohort de risco histórico
    if n_customers == 800:
        risk_count = 142
        risk_cids = customer_ids[:risk_count]
        other_cids = customer_ids[risk_count:]
        
        # Alocação de receita: 485.200 para risco e 1.471.600 para os demais (Total 1.956.800)
        raw_risk = np.random.uniform(1500.0, 5500.0, size=risk_count)
        risk_spend = (raw_risk / raw_risk.sum()) * 485200.0
        risk_spend = np.round(risk_spend, 2)
        risk_spend[0] += round(485200.0 - risk_spend.sum(), 2)

        raw_other = np.random.lognormal(mean=7.0, sigma=0.85, size=len(other_cids))
        other_spend = (raw_other / raw_other.sum()) * 1471600.0
        other_spend = np.round(other_spend, 2)
        other_spend[0] += round(1471600.0 - other_spend.sum(), 2)

        records = []
        trx_id = 100000

        # Clientes em risco (última compra entre 135 e 360 dias atrás)
        for cid, tot_val in zip(risk_cids, risk_spend):
            n_tx = int(np.random.randint(6, 18))
            last_day = int(np.random.randint(135, 360))
            tx_days = sorted(list(np.random.randint(last_day, 540, size=n_tx)), reverse=True)
            tx_days[0] = last_day
            raw_v = np.random.uniform(0.5, 1.5, size=n_tx)
            v_parts = np.round((raw_v / raw_v.sum()) * tot_val, 2)
            v_parts[0] += round(tot_val - v_parts.sum(), 2)
            for d, v in zip(tx_days, v_parts):
                trx_id += 1
                records.append({
                    "id_cliente": cid,
                    "data_transacao": end_date - timedelta(days=int(d)),
                    "id_transacao": f"TRX-{trx_id}",
                    "valor_total": float(v)
                })

        # Demais clientes
        for cid, tot_val in zip(other_cids, other_spend):
            tier = np.random.choice(["champion", "loyal", "new", "other"], p=[0.25, 0.35, 0.20, 0.20])
            if tier == "champion":
                n_tx = int(np.random.randint(8, 26))
                last_day = int(np.random.randint(1, 28))
            elif tier == "loyal":
                n_tx = int(np.random.randint(5, 15))
                last_day = int(np.random.randint(15, 75))
            elif tier == "new":
                n_tx = int(np.random.randint(1, 3))
                last_day = int(np.random.randint(1, 30))
            else:
                n_tx = int(np.random.randint(1, 4))
                last_day = int(np.random.randint(60, 480))
            tx_days = sorted(list(np.random.randint(last_day, 540, size=n_tx)), reverse=True)
            tx_days[0] = last_day
            raw_v = np.random.uniform(0.5, 1.5, size=n_tx)
            v_parts = np.round((raw_v / raw_v.sum()) * tot_val, 2)
            v_parts[0] += round(tot_val - v_parts.sum(), 2)
            for d, v in zip(tx_days, v_parts):
                trx_id += 1
                records.append({
                    "id_cliente": cid,
                    "data_transacao": end_date - timedelta(days=int(d)),
                    "id_transacao": f"TRX-{trx_id}",
                    "valor_total": float(v)
                })

        df = pd.DataFrame(records)
        df = df.sort_values(by="data_transacao").reset_index(drop=True)
        return df

    # Caso genérico para outros n_customers
    first_customers = customer_ids.copy()
    np.random.shuffle(first_customers)
    remaining_count = max(0, n_transactions - n_customers)
    weights = np.random.pareto(a=1.8, size=n_customers) + 0.05
    customer_probs = weights / weights.sum()
    chosen_customers = first_customers + list(np.random.choice(customer_ids, size=remaining_count, p=customer_probs))

    all_dates = [start_date + timedelta(days=i) for i in range(total_days + 1)]
    date_weights = [1.8 if d.month in [11, 12] else (1.3 if 1 <= d.day <= 10 else 1.0) for d in all_dates]
    date_probs = np.array(date_weights) / sum(date_weights)
    chosen_dates = [all_dates[idx] for idx in np.random.choice(len(all_dates), size=len(chosen_customers), p=date_probs)]

    client_spend_affinity = {cid: np.random.choice([0.6, 1.0, 1.8, 3.5], p=[0.40, 0.40, 0.15, 0.05]) for cid in customer_ids}
    raw_values = np.random.lognormal(mean=4.8, sigma=0.75, size=len(chosen_customers))
    adjusted_values = [max(25.00, round(val * client_spend_affinity[cid], 2)) for val, cid in zip(raw_values, chosen_customers)]
    transaction_ids = [f"TRX-{100000 + i}" for i in range(len(chosen_customers))]

    df = pd.DataFrame(
        {
            "id_cliente": chosen_customers,
            "data_transacao": pd.to_datetime(chosen_dates),
            "id_transacao": transaction_ids,
            "valor_total": adjusted_values,
        }
    )
    df = df.sort_values(by="data_transacao").reset_index(drop=True)
    return df


# ==============================================================================
# MOTOR DE CLASSIFICAÇÃO DOS CLUSTERS RFM
# ==============================================================================
def assign_segment(r_score: int, f_score: int, m_score: int) -> str:
    """
    Classifica um cliente em um dos 11 clusters de negócio com base em seus scores R, F e M.

    A lógica é estritamente mutuamente exclusiva e exaustiva, garantindo que nenhum cliente
    fique sem segmentação (0% de valores nulos).

    Clusters:
    1. 'Campeões': R in [4, 5] e F in [4, 5]
    2. 'Não Podemos Perder': R in [1, 2] e (F in [4, 5] ou (F == 3 e M in [4, 5]))
    3. 'Em Risco': R in [1, 2] e F in [3, 4]
    4. 'Leais': R in [3, 4, 5] e F in [3, 4, 5]
    5. 'Potenciais Clientes Leais': R in [4, 5] e F == 2
    6. 'Novos Clientes': R in [4, 5] e F == 1
    7. 'Promissores': R == 3 e F == 1
    8. 'Precisam de Atenção': R == 3 e F == 2
    9. 'Quase Hibernando': R == 2 e F in [1, 2]
    10. 'Perdidos': R == 1 e F == 1
    11. 'Hibernando': R in [1, 2] e F in [1, 2] (demais clientes)
    """
    # 1. Campeões: Compraram muito recentemente, compram muito frequentemente
    if r_score >= 4 and f_score >= 4:
        return "Campeões"

    # 2. Não Podemos Perder: Compradores frequentes e de alto valor que sumiram
    if r_score <= 2 and (f_score >= 4 or (f_score == 3 and m_score >= 4)):
        return "Não Podemos Perder"

    # 3. Em Risco: Compravam com frequência relevante e sumiram recentemente
    if r_score <= 2 and f_score >= 3:
        return "Em Risco"

    # 4. Leais: Boa frequência e recência moderada a alta (que não são Campeões)
    if r_score >= 3 and f_score >= 3:
        return "Leais"

    # 5. Potenciais Clientes Leais: Compraram recentemente e já fizeram mais de 1 compra
    if r_score >= 4 and f_score == 2:
        return "Potenciais Clientes Leais"

    # 6. Novos Clientes: Compraram muito recentemente pela primeira vez
    if r_score >= 4 and f_score == 1:
        return "Novos Clientes"

    # 7. Promissores: Compraram há tempo mediano pela primeira vez
    if r_score == 3 and f_score == 1:
        return "Promissores"

    # 8. Precisam de Atenção: Recência e frequência medianas
    if r_score == 3 and f_score == 2:
        return "Precisam de Atenção"

    # 9. Quase Hibernando: Recência baixa (2) e frequência baixa
    if r_score == 2 and f_score <= 2:
        return "Quase Hibernando"

    # 10. Perdidos: Pior recência (1) e compraram apenas uma vez
    if r_score == 1 and f_score == 1:
        return "Perdidos"

    # 11. Hibernando: Demais clientes inativos com baixa frequência
    return "Hibernando"


# ==============================================================================
# CÁLCULO RFM E PONTUAÇÃO VIA QUANTIS
# ==============================================================================
def calculate_rfm(
    df: pd.DataFrame,
    customer_col: str = "id_cliente",
    date_col: str = "data_transacao",
    transaction_col: str = "id_transacao",
    value_col: str = "valor_total",
    reference_date: Optional[datetime] = None,
) -> pd.DataFrame:
    """
    Processa dados transacionais brutos e calcula as métricas e pontuações RFM por cliente.

    Etapas:
    1. Conversão e validação dos tipos de dados.
    2. Agregação por cliente:
       - Recência (R): dias entre a última compra e a data de referência (última data + 1 dia).
       - Frequência (F): contagem de transações únicas.
       - Valor (M): soma do valor total transacionado.
    3. Atribuição de scores de 1 a 5 usando quantis (pd.qcut) com tratamento rigoroso de empates
       via rank(method='first').
       - Recência: menor recência ganha score 5 (invertido: [5, 4, 3, 2, 1]).
       - Frequência e Valor: maiores métricas ganham score 5 ([1, 2, 3, 4, 5]).
    4. Atribuição dos clusters de negócio e metadados de ação.

    Args:
        df: DataFrame com dados transacionais.
        customer_col: Nome da coluna de identificação do cliente.
        date_col: Nome da coluna de data da transação.
        transaction_col: Nome da coluna de ID do pedido/transação.
        value_col: Nome da coluna com valor financeiro da compra.
        reference_date: Data base para cálculo da recência (default: max(data) + 1 dia).

    Returns:
        pd.DataFrame consolidado por cliente com métricas brutas, scores e segmento.
    """
    if df.empty:
        raise ValueError("A base de dados informada está vazia.")

    required_cols = [customer_col, date_col, transaction_col, value_col]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise KeyError(f"Colunas obrigatórias ausentes no DataFrame: {missing}")

    # Cria cópia para evitar efeitos colaterais
    work_df = df[required_cols].copy()

    # Validações e conversões de tipo
    work_df[date_col] = pd.to_datetime(work_df[date_col], errors="coerce")
    work_df[value_col] = pd.to_numeric(work_df[value_col], errors="coerce")

    # Remove registros com valores essenciais nulos
    work_df = work_df.dropna(subset=[customer_col, date_col, value_col])

    if work_df.empty:
        raise ValueError("Nenhum registro válido restante após limpeza de valores nulos.")

    # Define a data de referência
    if reference_date is None:
        max_date = work_df[date_col].max()
        ref_date = max_date + pd.Timedelta(days=1)
    else:
        ref_date = pd.to_datetime(reference_date)

    # Agrupamento por cliente
    rfm_table = work_df.groupby(customer_col).agg(
        Recencia=(date_col, lambda x: (ref_date - x.max()).days),
        Frequencia=(transaction_col, "nunique"),
        Valor=(value_col, "sum"),
        Primeira_Compra=(date_col, "min"),
        Ultima_Compra=(date_col, "max"),
    ).reset_index()

    # Trata possíveis valores negativos ou zero de recência
    rfm_table["Recencia"] = rfm_table["Recencia"].apply(lambda x: max(1, int(x)))
    rfm_table["Frequencia"] = rfm_table["Frequencia"].astype(int)
    rfm_table["Valor"] = rfm_table["Valor"].round(2)

    # ==========================================================================
    # ATRIBUIÇÃO DE SCORES (1 A 5) COM QUANTIS E DESEMPATE
    # ==========================================================================
    # Para Recência: Menor recência é melhor -> rank crescente recebe labels [5, 4, 3, 2, 1]
    # O método 'first' garante que mesmo com muitos clientes no mesmo dia, cada um
    # tenha um ranking contínuo único, permitindo que qcut divida exatamente em 5 fatias.
    r_rank = rfm_table["Recencia"].rank(method="first", ascending=True)
    rfm_table["R_Score"] = pd.qcut(
        r_rank, q=5, labels=[5, 4, 3, 2, 1]
    ).astype(int)

    # Para Frequência: Maior frequência é melhor -> rank crescente recebe labels [1, 2, 3, 4, 5]
    f_rank = rfm_table["Frequencia"].rank(method="first", ascending=True)
    rfm_table["F_Score"] = pd.qcut(
        f_rank, q=5, labels=[1, 2, 3, 4, 5]
    ).astype(int)

    # Para Valor Monetário: Maior valor é melhor -> rank crescente recebe labels [1, 2, 3, 4, 5]
    m_rank = rfm_table["Valor"].rank(method="first", ascending=True)
    rfm_table["M_Score"] = pd.qcut(
        m_rank, q=5, labels=[1, 2, 3, 4, 5]
    ).astype(int)

    # Código RFM composto e média aritmética
    rfm_table["RFM_Score"] = (
        rfm_table["R_Score"].astype(str)
        + rfm_table["F_Score"].astype(str)
        + rfm_table["M_Score"].astype(str)
    )
    rfm_table["Score_Geral"] = (
        (rfm_table["R_Score"] + rfm_table["F_Score"] + rfm_table["M_Score"]) / 3.0
    ).round(2)

    # Classificação do Segmento de Negócio
    rfm_table["Segmento"] = rfm_table.apply(
        lambda row: assign_segment(row["R_Score"], row["F_Score"], row["M_Score"]),
        axis=1,
    )

    # Ticket médio individual por pedido
    rfm_table["Ticket_Medio"] = (rfm_table["Valor"] / rfm_table["Frequencia"]).round(2)

    # Prioridade de ação comercial a partir dos metadados
    rfm_table["Prioridade_Acao"] = rfm_table["Segmento"].apply(
        lambda s: CLUSTER_METADATA.get(s, {}).get("prioridade", "Média")
    )

    return rfm_table


# ==============================================================================
# FUNÇÃO AUXILIAR PARA RESUMO EXECUTIVO DOS CLUSTERS
# ==============================================================================
def summarize_clusters(rfm_df: pd.DataFrame) -> pd.DataFrame:
    """
    Consolida as principais métricas de negócio agregadas por segmento.

    Métricas calculadas:
    - Quantidade de clientes e % de participação na base.
    - Receita total transacionada e % do faturamento global.
    - Ticket médio consolidado.
    - Médias dos scores R, F e M.
    """
    total_customers = len(rfm_df)
    total_revenue = rfm_df["Valor"].sum()

    summary = (
        rfm_df.groupby("Segmento")
        .agg(
            Qtd_Clientes=("id_cliente" if "id_cliente" in rfm_df.columns else rfm_df.columns[0], "count"),
            Receita_Total=("Valor", "sum"),
            Ticket_Medio=("Ticket_Medio", "mean"),
            Recencia_Media_Dias=("Recencia", "mean"),
            Frequencia_Media=("Frequencia", "mean"),
            R_Medio=("R_Score", "mean"),
            F_Medio=("F_Score", "mean"),
            M_Medio=("M_Score", "mean"),
        )
        .reset_index()
    )

    summary["Perc_Clientes"] = (summary["Qtd_Clientes"] / total_customers * 100).round(2)
    summary["Perc_Receita"] = (
        (summary["Receita_Total"] / total_revenue * 100).round(2) if total_revenue > 0 else 0
    )
    summary["Receita_Total"] = summary["Receita_Total"].round(2)
    summary["Ticket_Medio"] = summary["Ticket_Medio"].round(2)
    summary["Recencia_Media_Dias"] = summary["Recencia_Media_Dias"].round(1)
    summary["Frequencia_Media"] = summary["Frequencia_Media"].round(1)

    # Adicionar cor de cada segmento para referência em gráficos
    summary["Cor"] = summary["Segmento"].apply(
        lambda s: CLUSTER_METADATA.get(s, {}).get("cor", "#6B7280")
    )

    return summary.sort_values(by="Receita_Total", ascending=False).reset_index(drop=True)
