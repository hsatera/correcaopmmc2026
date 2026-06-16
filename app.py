import streamlit as st
import pandas as pd
from supabase import create_client, Client

# Configurações da página
st.set_page_config(page_title="Avaliação PMMC", page_icon="📝", layout="centered")

# ---------------------------------------------------------
# Conexão Segura em Segundo Plano
# ---------------------------------------------------------
try:
    URL_SISTEMA = st.secrets["SUPABASE_URL"]
    CHAVE_SISTEMA = st.secrets["SUPABASE_KEY"]
    cliente_banco: Client = create_client(URL_SISTEMA, CHAVE_SISTEMA)
except Exception:
    st.error("Erro de conexão com o servidor de envio. Por favor, contate o administrador.")
    st.stop()

# ---------------------------------------------------------
# Matriz de Correção (Dados Internos Ocultos)
# ---------------------------------------------------------
MATRIZ_RESPOSTAS = {
    1: {"resp": "A", "tema": "Acesso Avançado", "dificuldade": "Intermediária", "dominios": ["Gestão e Organização do Processo de Trabalho", "Saúde Coletiva"]},
    2: {"resp": "D", "tema": "Indicador APS", "dificuldade": "Intermediária", "dominios": ["Gestão e Organização do Processo de Trabalho", "Avaliação da Qualidade e Auditoria", "Saúde Coletiva"]},
    3: {"resp": "D", "tema": "Avaliação – PCATool", "dificuldade": "Intermediária", "dominios": ["Princípios da APS", "Avaliação da Qualidade e Auditoria", "Saúde Coletiva"]},
    4: {"resp": "C", "tema": "Saúde Mental – SAA", "dificuldade": "Intermediária", "dominios": ["Atenção à Saúde"]},
    5: {"resp": "C", "tema": "Saúde Mental – Desprescrição", "dificuldade": "Fácil", "dominios": ["Atenção à Saúde"]},
    6: {"resp": "C", "tema": "Saúde Mental – Ideação Suicida", "dificuldade": "Fácil", "dominios": ["Atenção à Saúde"]},
    7: {"resp": "A", "tema": "Saúde Mental – Manejo Farmacológico", "dificuldade": "Intermediária", "dominios": ["Atenção à Saúde"]},
    8: {"resp": "C", "tema": "Pesquisa em Saúde", "dificuldade": "Fácil", "dominios": ["Pesquisa Médica", "Gestão em Saúde", "Comunicação e Docência"]},
    9: {"resp": "B", "tema": "Pesquisa em Saúde – CEP", "dificuldade": "Fácil", "dominios": ["Atenção à Saúde"]},
    10: {"resp": "C", "tema": "Planejamento Reprodutivo", "dificuldade": "Intermediária", "dominios": ["Atenção à Saúde"]},
    11: {"resp": "C", "tema": "Planejamento Reprodutivo", "dificuldade": "Intermediária", "dominios": ["Atenção à Saúde"]},
    12: {"resp": "C", "tema": "Abordagem Familiar", "dificuldade": "Intermediária", "dominios": ["Atenção à Saúde"]},
    13: {"resp": "C", "tema": "Genograma e Ecomapa", "dificuldade": "Fácil", "dominios": ["Atenção à Saúde"]},
    14: {"resp": "C", "tema": "Prevenção Quaternária", "dificuldade": "Fácil", "dominios": ["Atenção à Saúde", "Princípios da APS"]},
    15: {"resp": "C", "tema": "Rastreamento em APS", "dificuldade": "Intermediária", "dominios": ["Atenção à Saúde"]},
    16: {"resp": "C", "tema": "Rastreamento de CA de Colo de Útero", "dificuldade": "Intermediária", "dominios": ["Atenção à Saúde"]},
    17: {"resp": "D", "tema": "Rastreamento de CA de Mama", "dificuldade": "Intermediária", "dominios": ["Atenção à Saúde"]},
    18: {"resp": "A", "tema": "Diabetes Mellitus - Diagnóstico", "dificuldade": "Fácil", "dominios": ["Atenção à Saúde"]},
    19: {"resp": "C", "tema": "Diabetes Mellitus - Manejo", "dificuldade": "Intermediária", "dominios": ["Atenção à Saúde"]},
    20: {"resp": "B", "tema": "Hipertensão Arterial - Diagnóstico", "dificuldade": "Fácil", "dominios": ["Atenção à Saúde"]},
    21: {"resp": "D", "tema": "Hipertensão Arterial - Manejo", "dificuldade": "Intermediária", "dominios": ["Atenção à Saúde"]},
    22: {"resp": "D", "tema": "Dislipidemia", "dificuldade": "Intermediária", "dominios": ["Atenção à Saúde"]},
    23: {"resp": "D", "tema": "Asma - Manejo", "dificuldade": "Intermediária", "dominios": ["Atenção à Saúde"]},
    24: {"resp": "B", "tema": "DPOC - Manejo", "dificuldade": "Intermediária", "dominios": ["Atenção à Saúde"]},
    25: {"resp": "D", "tema": "Insuficiência Cardíaca", "dificuldade": "Intermediária", "dominios": ["Atenção à Saúde"]},
    26: {"resp": "A", "tema": "Puericultura - Desenvolvimento", "dificuldade": "Fácil", "dominios": ["Atenção à Saúde"]},
    27: {"resp": "A", "tema": "Puericultura - Crescimento", "dificuldade": "Fácil", "dominios": ["Atenção à Saúde"]},
    28: {"resp": "B", "tema": "Infecções de Vias Aéreas Superiores", "dificuldade": "Fácil", "dominios": ["Atenção à Saúde"]},
    29: {"resp": "C", "tema": "Infecção do Trato Urinário - Pediatria", "dificuldade": "Intermediária", "dominios": ["Atenção à Saúde"]},
    30: {"resp": "D", "tema": "Anemia Ferropriva na Infância", "dificuldade": "Fácil", "dominios": ["Atenção à Saúde"]},
    31: {"resp": "B", "tema": "Pré-Natal de Baixo Risco", "dificuldade": "Fácil", "dominios": ["Atenção à Saúde"]},
    32: {"resp": "C", "tema": "Sangramento Uterino Anormal", "dificuldade": "Intermediária", "dominios": ["Atenção à Saúde"]},
    33: {"resp": "D", "tema": "Climatério e Menopausa", "dificuldade": "Intermediária", "dominios": ["Atenção à Saúde"]},
    34: {"resp": "A", "tema": "Vulnerabilidades e Saúde LGBT+", "dificuldade": "Fácil", "dominios": ["Atenção à Saúde", "Saúde Coletiva"]},
    35: {"resp": "B", "tema": "Dermatologia na APS", "dificuldade": "Intermediária", "dominios": ["Atenção à Saúde"]},
    36: {"resp": "C", "tema": "Lombalgia Crônica", "dificuldade": "Fácil", "dominios": ["Atenção à Saúde"]},
    37: {"resp": "C", "tema": "Polifarmácia no Idoso", "dificuldade": "Intermediária", "dominios": ["Atenção à Saúde"]},
    38: {"resp": "A", "tema": "Cuidados Paliativos na APS", "dificuldade": "Fácil", "dominios": ["Atenção à Saúde"]},
    39: {"resp": "B", "tema": "Notificação Compulsória", "dificuldade": "Fácil", "dominios": ["Saúde Coletiva"]},
    40: {"resp": "B", "tema": "HAS - MRPA", "dificuldade": "Intermediária", "dominios": ["Atenção à Saúde"]}
}

# Cabeçalho Oficial da Prova
st.title("📝 AVALIAÇÃO PMMC JUNHO 2026")
st.markdown("Selecione os seus dados de identificação e preencha as alternativas escolhidas para cada questão.")

# ---------------------------------------------------------
# Identificação do Residente
# ---------------------------------------------------------
st.subheader("👤 Identificação")
c1, c2 = st.columns(2)
with c1:
    nivel_residencia = st.selectbox("Nível:", ["R1", "R2"])
with c2:
    instituicao = st.selectbox("Instituição:", ["PMC-CHOV", "Unicamp", "PUCCAMP", "PMC-Gatti"])

st.divider()

# ---------------------------------------------------------
# Painel de Respostas (Mobile-Friendly)
# ---------------------------------------------------------
st.subheader("📋 Painel de Questões")
respostas_inseridas = {}

for numero_q in range(1, 41):
    respostas_inseridas[numero_q] = st.radio(
        "",  # Nome do preenchimento removido (label vazio)
        ["A", "B", "C", "D"],
        index=0,  # Letra A pré-marcada por padrão
        key=f"q_{numero_q}",
        horizontal=True
    )

st.divider()

# Botão de Envio
if st.button("📊 Emitir Boletim", type="primary", use_container_width=True):
    pendentes = [q for q, resp in respostas_inseridas.items() if resp is None]
    
    if pendentes:
        st.error(f"Por favor, selecione uma alternative para todas as questões antes de prosseguir. Pendentes: {pendentes}")
    else:
        total_acertos = 0
        dados_detalhados = []
        indicadores_dificuldade = {"Fácil": {"acertos": 0, "total": 0}, "Intermediária": {"acertos": 0, "total": 0}}
        indicadores_dominios = {}

        for q, alternativa_usuario in respostas_inseridas.items():
            dados_referencia = MATRIZ_RESPOSTAS[q]
            correto = (alternativa_usuario == dados_referencia["resp"])
            
            if correto:
                total_acertos += 1
            
            nivel_dif = dados_referencia["dificuldade"]
            indicadores_dificuldade[nivel_dif]["total"] += 1
            if correto:
                indicadores_dificuldade[nivel_dif]["acertos"] += 1
                
            for dom in dados_referencia["dominios"]:
                if dom not in indicadores_dominios:
                    indicadores_dominios[dom] = {"acertos": 0, "total": 0}
                indicadores_dominios[dom]["total"] += 1
                if correto:
                    indicadores_dominios[dom]["acertos"] += 1

            dados_detalhados.append({
                "Questão": q,
                "Tema": dados_referencia["tema"],
                "Sua Escolha": alternativa_usuario,
                "Situação": "Correto" if correto else "Incorreto"
            })

        # ---------------------------------------------------------
        # Armazenamento Seguro de Dados (Invisível ao Aluno)
        # ---------------------------------------------------------
        respostas_finais_banco = {str(k): v for k, v in respostas_inseridas.items()}
        dados_registro = {
            "residente_nivel": nivel_residencia,
            "instituicao": instituicao,
            "acertos": total_acertos,
            "respostas_usuario": respostas_finais_banco
        }
        
        try:
            cliente_banco.table("respostas_simulado").insert(dados_registro).execute()
        except Exception:
            pass

        # ---------------------------------------------------------
        # Exibição Final do Boletim do Aluno
        # ---------------------------------------------------------
        st.header("📋 Boletim")
        st.metric("Sua Nota", f"{(total_acertos / 40) * 10:.1f} / 10.0")
        st.metric("Total de Acertos", f"{total_acertos} de 40")
        st.metric("Aproveitamento", f"{(total_acertos / 40) * 100:.1f}%")

        st.divider()
        st.subheader("📈 Desempenho por Categorias")
        
        st.write("**Por Complexidade das Questões:**")
        for dif, valores in indicadores_dificuldade.items():
            porcentagem = (valores["acertos"] / valores["total"]) * 100 if valores["total"] > 0 else 0
            st.write(f"- *Nível {dif}*: {valores['acertos']}/{valores['total']} ({porcentagem:.1f}%)")
            st.progress(porcentagem / 100)

        st.divider()
        st.write("**Por Domínio de Competência:**")
        for dom, valores in indicadores_dominios.items():
            porcentagem = (valores["acertos"] / valores["total"]) * 100 if valores["total"] > 0 else 0
            st.write(f"- *{dom}*: {valores['acertos']}/{valores['total']} ({porcentagem:.1f}%)")
            st.progress(porcentagem / 100)

        st.divider()
        st.subheader("🔍 Espelho de Respostas")
        df_final = pd.DataFrame(dados_detalhados)
        st.dataframe(df_final.set_index("Questão"), use_container_width=True)

# ---------------------------------------------------------
# PAINEL DE RESULTADOS - RESERVADO PARA PRECEPTORES (COM SENHA)
# ---------------------------------------------------------
st.markdown("<br><br><br><hr>", unsafe_allow_html=True)
st.subheader("🔐 Área Restrita - Painel de Resultados")

senha_painel = st.text_input("Digite a senha de acesso institucional:", type="password")

if senha_painel == "Correcao2026@":
    st.success("Acesso autorizado!")
    
    # Busca dados no Supabase de forma otimizada
    try:
        resposta_bd = cliente_banco.table("respostas_simulado").select("*").execute()
        dados_alunos = resposta_bd.data
    except Exception:
        dados_alunos = []
        st.error("Não foi possível conectar para puxar as estatísticas gerais do banco.")

    if dados_alunos:
        # Estrutura base de dados coletados
        df_bd = pd.DataFrame(dados_alunos)
        
        # Extrair ano da data_envio se disponível, caso contrário assume 2026
        if 'data_envio' in df_bd.columns:
            df_bd['ano'] = pd.to_datetime(df_bd['data_envio']).dt.year.astype(str)
        else:
            df_bd['ano'] = "2026"

        # ---------------------------------------------------------
        # Seção de Filtros Globais do Painel
        # ---------------------------------------------------------
        st.markdown("### 🎛️ Filtros Avançados de Análise")
        fl1, fl2 = st.columns(2)
        with fl1:
            filtro_ano = st.multiselect("Filtrar por Ano:", options=list(df_bd['ano'].unique()), default=list(df_bd['ano'].unique()))
            filtro_inst = st.multiselect("Filtrar por Instituição:", options=list(df_bd['instituicao'].unique()), default=list(df_bd['instituicao'].unique()))
        with fl2:
            todos_dominios_lista = sorted(list(set([d for q in MATRIZ_RESPOSTAS.values() for d in q["dominios"]])))
            filtro_dom = st.multiselect("Filtrar por Domínio da Questão:", options=todos_dominios_lista, default=todos_dominios_lista)
            filtro_q = st.multiselect("Filtrar por Questão Específica:", options=list(range(1, 41)), default=list(range(1, 41)))

        # Aplicando filtros de Aluno (Ano e Instituição)
        df_filtrado = df_bd[(df_bd['ano'].isin(filtro_ano)) & (df_bd['instituicao'].isin(filtro_inst))]

        # Processamento Estatístico Geral por Questão
        total_respondentes = len(df_filtrado)
        
        estatisticas_questoes = []
        for q_num, info_matriz in MATRIZ_RESPOSTAS.items():
            # Filtro por escopo de questão selecionado
            if q_num not in filtro_q:
                continue
            # Filtro por escopo de domínio selecionado
            if not any(d in filtro_dom for d in info_matriz["dominios"]):
                continue
                
            acertos_q = 0
            for idx, row in df_filtrado.iterrows():
                respostas_dict = row['respostas_usuario']
                if respostas_dict and respostas_dict.get(str(q_num)) == info_matriz["resp"]:
                    acertos_q += 1
            
            pct_acerto = (acertos_q / total_respondentes * 100) if total_respondentes > 0 else 0
            
            # Cálculo de discriminação simples (Ex: <30% ruim, 30-70% média, >70% boa retenção)
            if pct_acerto < 35:
                discrimina = "Alta Dificuldade / Revisar Conteúdo"
            elif pct_acerto > 85:
                discrimina = "Excelente Retenção / Domínio Consolidado"
            else:
                discrimina = "Esperada / Balanceada"

            estatisticas_questoes.append({
                "Questão": q_num,
                "Tema": info_matriz["tema"],
                "Dificuldade": info_matriz["dificuldade"],
                "Domínios": ", ".join(info_matriz["dominios"]),
                "% Acerto": round(pct_acerto, 1),
                "Discriminação": discrimina
            })

        df_analise_questoes = pd.DataFrame(estatisticas_questoes)

        # ---------------------------------------------------------
        # SEÇÃO 1: Comparativo e Totalizadores
        # ---------------------------------------------------------
        st.divider()
        st.markdown("### 📊 Seção 1: Comparativo de Participação")
        
        m1, m2 = st.columns(2)
        m1.metric("Total de Respondentes (Filtro Atual)", total_respondentes)
        if total_respondentes > 0:
            m2.metric("Média Geral de Acertos", f"{round(df_filtrado['acertos'].mean(), 1)} / 40")

        if total_respondentes > 0:
            st.write("**Participação por Instituição:**")
            st.bar_chart(df_filtrado['instituicao'].value_counts())

        # ---------------------------------------------------------
        # SEÇÃO 2: Métricas por Questão, Dificuldade e Domínio
        # ---------------------------------------------------------
        st.divider()
        st.markdown("### 🎯 Seção 2: Desempenho Técnico por Questão")
        
        if not df_analise_questoes.empty:
            st.write("**Tabela de Métricas e Discriminação de Itens:**")
            st.dataframe(df_analise_questoes.set_index("Questão"), use_container_width=True)
            
            # Gráfico rápido de % de acerto por questão filtrada
            st.write("**Gráfico de Rendimento (% de Acertos por Questão):**")
            st.line_chart(df_analise_questoes.set_index("Questão")["% Acerto"])
        else:
            st.warning("Nenhuma questão corresponde aos filtros selecionados acima.")
            
    else:
        st.info("O banco de dados ainda está vazio ou nenhum registro coincide com os parâmetros básicos.")
elif senha_painel != "":
    st.error("Senha incorreta. Acesso negado.")
