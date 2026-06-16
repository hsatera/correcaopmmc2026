import streamlit as str
import pandas as pd
from supabase import create_client, Client

# Configurações da página
str.set_page_config(page_title="Avaliação PMMC", page_icon="📝", layout="centered")

# ---------------------------------------------------------
# Conexão Segura em Segundo Plano
# ---------------------------------------------------------
try:
    URL_SISTEMA = str.secrets["SUPABASE_URL"]
    CHAVE_SISTEMA = str.secrets["SUPABASE_KEY"]
    cliente_banco: Client = create_client(URL_SISTEMA, CHAVE_SISTEMA)
except Exception:
    str.error("Erro de conexão com o servidor de envio. Por favor, contate o administrador.")
    str.stop()

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
str.title("📝 AVALIAÇÃO PMMC JUNHO 2026")
str.markdown("Selecione os seus dados de identificação e preencha as alternativas escolhidas para cada questão.")

# ---------------------------------------------------------
# Identificação do Residente (Dropdowns no Corpo do Site)
# ---------------------------------------------------------
str.subheader("👤 Identificação")

c1, c2 = str.columns(2)
with c1:
    nivel_residencia = str.selectbox("Nível:", ["R1", "R2"])
with c2:
    instituicao = str.selectbox("Instituição:", ["PMC-CHOV", "Unicamp", "PUCCAMP", "PMC-Gatti"])

str.divider()

# ---------------------------------------------------------
# Painel de Respostas (Mobile-Friendly)
# ---------------------------------------------------------
str.subheader("📋 Painel de Questões")

respostas_inseridas = {}

for numero_q in range(1, 41):
    respostas_inseridas[numero_q] = str.radio(
        f"Questão {numero_q:02d}:",
        ["A", "B", "C", "D"],
        index=None,
        key=f"q_{numero_q}",
        horizontal=True
    )

str.divider()

# Botão de Envio
if str.button("📊 Emitir Boletim", type="primary", use_container_width=True):
    pendentes = [q for q, resp in respostas_inseridas.items() if resp is None]
    
    if pendentes:
        str.error(f"Por favor, selecione uma alternativa para todas as questões antes de prosseguir. Pendentes: {pendentes}")
    else:
        # Processamento Interno do Desempenho
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
        # Exibição Final do Boletim
        # ---------------------------------------------------------
        str.header("📋 Boletim")
        
        str.metric("Sua Nota", f"{(total_acertos / 40) * 10:.1f} / 10.0")
        str.metric("Total de Acertos", f"{total_acertos} de 40")
        str.metric("Aproveitamento", f"{(total_acertos / 40) * 100:.1f}%")

        str.divider()
        str.subheader("📈 Desempenho por Categorias")
        
        str.write("**Por Complexidade das Questões:**")
        for dif, valores in indicadores_dificuldade.items():
            porcentagem = (valores["acertos"] / valores["total"]) * 100 if valores["total"] > 0 else 0
            str.write(f"- *Nível {dif}*: {valores['acertos']}/{valores['total']} ({porcentagem:.1f}%)")
            str.progress(porcentagem / 100)

        str.divider()
        str.write("**Por Domínio de Competência:**")
        for dom, valores in indicadores_dominios.items():
            porcentagem = (valores["acertos"] / valores["total"]) * 100 if valores["total"] > 0 else 0
            str.write(f"- *{dom}*: {valores['acertos']}/{valores['total']} ({porcentagem:.1f}%)")
            str.progress(porcentagem / 100)

        str.divider()
        str.subheader("🔍 Espelho de Respostas")
        df_final = pd.DataFrame(dados_detalhados)
        str.dataframe(df_final.set_index("Questão"), use_container_width=True)
