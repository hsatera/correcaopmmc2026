import streamlit as st
import pandas as pd
import numpy as np
from supabase import create_client, Client

# Configurações da página
st.set_page_config(page_title="Avaliação PMMC", page_icon="📝", layout="wide")

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

# ---------------------------------------------------------
# Menu de Navegação no Lado Esquerdo (Sidebar)
# ---------------------------------------------------------
st.sidebar.title("📌 Menu de Navegação")
pagina_selecionada = st.sidebar.radio(
    "Ir para a seção:",
    ["📝 Responder Simulado", "📊 Boletim Geral (Preceptores)"]
)

# ---------------------------------------------------------
# SEÇÃO 1: RESPONDER SIMULADO
# ---------------------------------------------------------
if pagina_selecionada == "📝 Responder Simulado":
    st.title("📝 AVALIAÇÃO PMMC JUNHO 2026")
    st.markdown("Selecione os seus dados de identificação e preencha as alternativas escolhidas para cada questão.")

    st.subheader("👤 Identificação")
    c1, c2 = st.columns(2)
    with c1:
        nivel_residencia = st.selectbox("Nível:", ["R1", "R2"])
    with c2:
        instituicao = st.selectbox("Instituição:", ["PMC-CHOV", "Unicamp", "PUCCAMP", "PMC-Gatti"])

    st.divider()

    st.subheader("📋 Painel de Questões")
    respostas_inseridas = {}

    # Layout em colunas para ocupar menos espaço vertical na folha de respostas
    for numero_q in range(1, 41):
        respostas_inseridas[numero_q] = st.radio(
            f"Questão {numero_q}", 
            ["A", "B", "C", "D"],
            index=0,
            key=f"q_{numero_q}",
            horizontal=True
        )

    st.divider()

    if st.button("📊 Emitir Meu Boletim Individual", type="primary", use_container_width=True):
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
                "Gabarito": dados_referencia["resp"],
                "Situação": "🟢 Correto" if correto else "🔴 Incorreto"
            })

        # Armazenamento Seguro de Dados (Invisível ao Aluno)
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

        # Exibição Final do Boletim do Aluno
        st.header("📋 Seu Resultado Individual")
        col_b1, col_b2, col_b3 = st.columns(3)
        col_b1.metric("Sua Nota", f"{(total_acertos / 40) * 10:.1f} / 10.0")
        col_b2.metric("Total de Acertos", f"{total_acertos} de 40")
        col_b3.metric("Aproveitamento", f"{(total_acertos / 40) * 100:.1f}%")

        st.divider()
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.write("**Desempenho por Complexidade:**")
            for dif, valores in indicadores_dificuldade.items():
                pct = (valores["acertos"] / valores["total"]) * 100 if valores["total"] > 0 else 0
                st.write(f"- *Nível {dif}*: {valores['acertos']}/{valores['total']} ({pct:.1f}%)")
                st.progress(pct / 100)
                
        with col_g2:
            st.write("**Desempenho por Domínio de Competência:**")
            for dom, valores in indicadores_dominios.items():
                pct = (valores["acertos"] / valores["total"]) * 100 if valores["total"] > 0 else 0
                st.write(f"- *{dom}*: {valores['acertos']}/{valores['total']} ({pct:.1f}%)")
                st.progress(pct / 100)

        st.divider()
        st.subheader("🔍 Espelho da Prova")
        df_final = pd.DataFrame(dados_detalhados)
        st.dataframe(df_final.set_index("Questão"), use_container_width=True)

# ---------------------------------------------------------
# SEÇÃO 2: PAINEL DE RESULTADOS (BOLETIM GERAL)
# ---------------------------------------------------------
elif pagina_selecionada == "📊 Boletim Geral (Preceptores)":
    st.title("📊 Boletim Analítico e Painel de Resultados")
    st.markdown("Acesso exclusivo para preceptores e coordenadores da avaliação médica.")
    
    senha_painel = st.text_input("Digite a senha de acesso institucional:", type="password")

    if senha_painel == "Correcao2026@":
        st.success("Acesso autorizado de nível institucional!")
        
        # Puxa os dados do Supabase
        try:
            resposta_bd = cliente_banco.table("respostas_simulado").select("*").execute()
            dados_alunos = resposta_bd.data
        except Exception:
            dados_alunos = []
            st.error("Erro crítico ao obter informações do banco de dados.")

        if dados_alunos:
            df_bd = pd.DataFrame(dados_alunos)
            
            if 'data_envio' in df_bd.columns:
                df_bd['ano'] = pd.to_datetime(df_bd['data_envio']).dt.year.astype(str)
            else:
                df_bd['ano'] = "2026"

            # ---------------------------------------------------------
            # Painel de Filtros Superiores
            # ---------------------------------------------------------
            st.markdown("### 🎛️ Filtros Avançados")
            fl1, fl2 = st.columns(2)
            with fl1:
                filtro_ano = st.multiselect("Filtrar por Ano da Prova:", options=list(df_bd['ano'].unique()), default=list(df_bd['ano'].unique()))
                filtro_inst = st.multiselect("Filtrar por Instituição do Residente:", options=list(df_bd['instituicao'].unique()), default=list(df_bd['instituicao'].unique()))
            with fl2:
                filtro_nivel = st.multiselect("Filtrar por Ano de Residência:", options=list(df_bd['residente_nivel'].unique()), default=list(df_bd['residente_nivel'].unique()))
                filtro_q = st.multiselect("Filtrar Questões no Painel:", options=list(range(1, 41)), default=list(range(1, 41)))

            # Aplicando os Filtros
            df_filtrado = df_bd[
                (df_bd['ano'].isin(filtro_ano)) & 
                (df_bd['instituicao'].isin(filtro_inst)) &
                (df_bd['residente_nivel'].isin(filtro_nivel))
            ]

            total_respondentes = len(df_filtrado)

            if total_respondentes > 0:
                # ---------------------------------------------------------
                # 1. RESUMO GERAL DE DESEMPENHO
                # ---------------------------------------------------------
                st.divider()
                st.subheader("📈 1. Resumo Geral Consolidador")
                
                c_res1, c_res2, c_res3 = st.columns(3)
                media_acertos = df_filtrado['acertos'].mean()
                c_res1.metric("Total de Alunos Avaliados", f"{total_respondentes} residentes")
                c_res2.metric("Média Geral de Acertos", f"{media_acertos:.1f} / 40 questões")
                c_res3.metric("Nota Média do Grupo", f"{(media_acertos / 40) * 10:.2f} / 10.0")

                # ---------------------------------------------------------
                # 2. DESEMPENHO POR INSTITUIÇÃO
                # ---------------------------------------------------------
                st.divider()
                st.subheader("🏢 2. Rendimento por Instituição de Ensino")
                
                resumo_inst = df_filtrado.groupby('instituicao').agg(
                    Total_Alunos=('acertos', 'count'),
                    Media_Acertos=('acertos', 'mean'),
                    Nota_Media=('acertos', lambda x: (x.mean() / 40) * 10)
                ).reset_index()
                
                resumo_inst['Aproveitamento (%)'] = (resumo_inst['Media_Acertos'] / 40) * 100
                resumo_inst = resumo_inst.rename(columns={
                    'instituicao': 'Instituição',
                    'Total_Alunos': 'Nº de Respondentes',
                    'Media_Acertos': 'Média de Acertos',
                    'Nota_Media': 'Nota Média (0-10)'
                })
                st.dataframe(resumo_inst.set_index('Instituição').style.format({'Média de Acertos': '{:.1f}', 'Nota Média (0-10)': '{:.2f}', 'Aproveitamento (%)': '{:.1f}%'}), use_container_width=True)

                # ---------------------------------------------------------
                # 3. DESEMPENHO POR NÍVEL (R1/R2)
                # ---------------------------------------------------------
                st.divider()
                st.subheader("🎓 3. Rendimento por Nível de Residência (R1 vs R2)")
                
                resumo_nivel = df_filtrado.groupby('residente_nivel').agg(
                    Total_Alunos=('acertos', 'count'),
                    Media_Acertos=('acertos', 'mean')
                ).reset_index()
                resumo_nivel['Aproveitamento (%)'] = (resumo_nivel['Media_Acertos'] / 40) * 100
                resumo_nivel = resumo_nivel.rename(columns={'residente_nivel': 'Nível Residência', 'Total_Alunos': 'Qtd Alunos', 'Media_Acertos': 'Média de Acertos'})
                
                st.dataframe(resumo_nivel.set_index('Nível Residência').style.format({'Média de Acertos': '{:.1f}', 'Aproveitamento (%)': '{:.1f}%'}), use_container_width=True)

                # ---------------------------------------------------------
                # PROCESSAMENTO POR ITEM (Dificuldade, Domínio e Discriminação TRI)
                # ---------------------------------------------------------
                # Cálculo dos grupos superior e inferior para achar a taxa de discriminação real (TRI clássica)
                # Separa os top 27% alunos com maiores notas e bottom 27% alunos com menores notas
                notas_ordenadas = df_filtrado.sort_values(by='acertos', ascending=False)
                tamanho_grupo = max(1, int(round(total_respondentes * 0.27)))
                grupo_superior = notas_ordenadas.head(tamanho_grupo)
                grupo_inferior = notas_ordenadas.tail(tamanho_grupo)

                estatisticas_questoes = []
                comp_dificuldade = {}
                comp_dominios = {}

                for q_num, info_matriz in MATRIZ_RESPOSTAS.items():
                    # Filtro de questões selecionadas pelo usuário na tela
                    if q_num not in filtro_q:
                        continue
                    
                    # Contagem de acertos geral, no grupo superior e inferior
                    acertos_geral = 0
                    acertos_sup = 0
                    acertos_inf = 0

                    for _, row in df_filtrado.iterrows():
                        if row['respostas_usuario'].get(str(q_num)) == info_matriz["resp"]: acertos_geral += 1
                    for _, row in grupo_superior.iterrows():
                        if row['respostas_usuario'].get(str(q_num)) == info_matriz["resp"]: acertos_sup += 1
                    for _, row in grupo_inferior.iterrows():
                        if row['respostas_usuario'].get(str(q_num)) == info_matriz["resp"]: acertos_inf += 1

                    pct_geral = (acertos_geral / total_respondentes) * 100
                    pct_sup = (acertos_sup / tamanho_grupo) * 100
                    pct_inf = (acertos_inf / tamanho_grupo) * 100
                    
                    # Índice de Discriminação (D = % Acerto Sup - % Acerto Inf)
                    taxa_discriminacao = (pct_sup - pct_inf) / 100

                    if taxa_discriminacao >= 0.40: class_dis = "Excelente Item"
                    elif taxa_discriminacao >= 0.30: class_dis = "Boa Discriminação"
                    elif taxa_discriminacao >= 0.20: class_dis = "Médio Limiar"
                    elif taxa_discriminacao < 0: class_dis = "⚠️ Inversa (Rever Gabarito)"
                    else: class_dis = "Fraca Discriminação"

                    # Agrega por nível de dificuldade
                    dif = info_matriz["dificuldade"]
                    if dif not in comp_dificuldade: comp_dificuldade[dif] = []
                    comp_dificuldade[dif].append(pct_geral)

                    # Agrega por domínios
                    for d in info_matriz["dominios"]:
                        if d not in comp_dominios: comp_dominios[d] = []
                        comp_dominios[d].append(pct_geral)

                    estatisticas_questoes.append({
                        "Questão": q_num,
                        "Tema": info_matriz["tema"],
                        "Dificuldade": dif,
                        "Domínios": ", ".join(info_matriz["dominios"]),
                        "% Acerto Geral": round(pct_geral, 1),
                        "Índice Discriminação": round(taxa_discriminacao, 2),
                        "Avaliação TRI": class_dis
                    })

                df_analise_questoes = pd.DataFrame(estatisticas_questoes)

                # ---------------------------------------------------------
                # 4. DESEMPENHO POR DIFICULDADE
                # ---------------------------------------------------------
                st.divider()
                st.subheader("📊 4. Rendimento por Nível de Dificuldade de Questão")
                dif_data = [{"Dificuldade": k, "Média de Acerto (%)": np.mean(v)} for k, v in comp_dificuldade.items()]
                st.dataframe(pd.DataFrame(dif_data).set_index("Dificuldade").style.format({'Média de Acerto (%)': '{:.1f}%'}), use_container_width=True)

                # ---------------------------------------------------------
                # 5. DESEMPENHO POR DOMÍNIO
                # ---------------------------------------------------------
                st.divider()
                st.subheader("🎯 5. Aproveitamento por Domínio de Competência")
                dom_data = [{"Domínio de Conhecimento": k, "Média de Acerto Grupo (%)": np.mean(v)} for k, v in comp_dominios.items()]
                st.dataframe(pd.DataFrame(dom_data).set_index("Domínio de Conhecimento").style.format({'Média de Acerto Grupo (%)': '{:.1f}%'}), use_container_width=True)

                # ---------------------------------------------------------
                # 6. DISCRIMINAÇÃO POR QUESTÃO
                # ---------------------------------------------------------
                st.divider()
                st.subheader("🔍 6. Espelho Detalhado de Itens e Taxa de Discriminação (TRI)")
                st.markdown("""
                *O **Índice de Discriminação** mede a capacidade da questão de distinguir alunos de alto rendimento dos de baixo rendimento. 
                Valores acima de **0.30** são ideais. Valores **negativos** indicam que alunos com notas menores acertaram mais que os alunos com notas maiores (necessita revisão).*
                """)
                st.dataframe(df_analise_questoes.set_index("Questão"), use_container_width=True)

                # Gráfico de Rendimento
                st.write("**Gráfico de Rendimento Linear por Questão (% de Acertos):**")
                st.line_chart(df_analise_questoes.set_index("Questão")["% Acerto Geral"])

            else:
                st.warning("Nenhum registro coincide com os filtros selecionados nos parâmetros acima.")
        else:
            st.info("Nenhuma resposta foi gravada no banco de dados ainda.")
    elif senha_painel != "":
        st.error("Senha institucional incorreta. Acesso negado à área de boletins.")
