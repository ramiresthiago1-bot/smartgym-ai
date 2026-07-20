import streamlit as st
import pandas as pd

# CONFIGURAÇÃO DA PÁGINA (Deve ser o primeiro comando Streamlit)
st.set_page_config(page_title="SmartGym AI", page_icon="🏋️‍♂️", layout="centered")

# TÍTULO PRINCIPAL
st.title("🏋️‍♂️ SmartGym AI")
st.subheader("Sistema Inteligente de Treino e Análise de Retenção")
st.write("Insira os dados do membro para gerar o treino ideal e calcular o risco de desistência.")

# --- SIDEBAR: ENTRADA DE DADOS ---
st.sidebar.header("📝 Dados do Membro")
nome = st.sidebar.text_input("Nome do Aluno", "João Silva")
idade = st.sidebar.slider("Idade", 16, 90, 30)
peso = st.sidebar.number_input("Peso (kg)", min_value=40.0, max_value=200.0, value=75.0)

objetivo = st.sidebar.selectbox(
    "Objetivo Principal", 
    ["Hipertrofia (Ganho de Massa)", "Emagrecimento", "Condicionamento Físico", "Saúde/Qualidade de Vida"]
)

frequencia_semanal = st.sidebar.slider("Frequência Semanal Recomendada/Desejada (Dias)", 1, 7, 3)
nivel_fadiga = st.sidebar.slider("Nível de Fadiga Atual (1 = Baixo, 5 = Muito Alto)", 1, 5, 2)

# --- BOTÃO DE PROCESSAMENTO ---
if st.sidebar.button("📊 Analisar e Gerar Plano"):
    
    st.markdown("---")
    st.header(f"📋 Relatório de Avaliação: {nome}")
    
    # 1. LÓGICA DO ALGORITMO PREDITIVO (Substituindo o Scikit-Learn por Score Lógico)
    # Quanto menor a frequência e maior a fadiga, maior o risco de o aluno abandonar a academia.
    score_risco = 0
    
    if frequencia_semanal <= 2:
        score_risco += 40
    elif frequencia_semanal == 3:
        score_risco += 20
        
    if nivel_fadiga >= 4:
        score_risco += 40
    elif nivel_fadiga == 3:
        score_risco += 15
        
    if idade < 21 or idade > 60:
        score_risco += 10 # Grupos que estatisticamente têm maior oscilação de frequência
        
    # Garantir limite de 0 a 100%
    porcentagem_risco = min(max(score_risco, 5), 95) 
    
    # Exibindo a Métrica de Risco (Usando componentes nativos do Streamlit)
    col1, col2 = st.columns(2)
    
    with col1:
        if porcentagem_risco >= 60:
            st.error(f"⚠️ Risco de Desistência: {porcentagem_risco}% (Alto Risco)")
        elif porcentagem_risco >= 30:
            st.warning(f"🟡 Risco de Desistência: {porcentagem_risco}% (Médio Risco)")
        else:
            st.success(f"🟢 Risco de Desistência: {porcentagem_risco}% (Baixo Risco)")
            
    with col2:
        st.metric(label="Frequência Alvo", value=f"{frequencia_semanal}x por semana")

    # 2. AUTOMAÇÃO DE RECOMENDAÇÃO DE TREINOS
    st.subheader("💪 Recomendação de Treino Automatizada")
    
    if nivel_fadiga >= 4:
        st.info("ℹ️ **Nota do Sistema AI:** O aluno apresenta fadiga elevada. O treino gerado foi adaptado para foco em recuperação e menor volume de carga.")
        tipo_treino = "Treino Regenerativo e Mobilidade"
        exercicios = ["10 min Esteira (Caminhada Leve)", "Alongamento Dinâmico Geral", "Leg Press 45° (Carga Leve) - 3x12", "Puxada Alta (Carga Moderada) - 3x10"]
    else:
        if objetivo == "Hipertrofia (Ganho de Massa)":
            tipo_treino = "Foco em Volume de Carga (Hipertrofia)"
            exercicios = ["5 min Aquecimento", "Agachamento Livre - 4x8", "Supino Reto - 4x10", "Remada Curvada - 4x10", "Desenvolvimento Halteres - 3x12"]
        elif objetivo == "Emagrecimento":
            tipo_treino = "Foco em Alta Intensidade e Condicionamento (Circuito)"
            exercicios = ["15 min HIIT na Bicicleta", "Afundo Avanço - 3x15", "Flexão de Braço - 3x Max", "Prancha Abdominal - 3x 45s", "Burpees - 3x10"]
        else:
            tipo_treino = "Treino Funcional e Resistência"
            exercicios = ["10 min Corrida Moderada", "Agachamento Sumô - 3x15", "Puxada no Triângulo - 3x12", "Elevação Lateral - 3x15"]
            
    st.markdown(f"**Plano focado em:** {tipo_treino}")
    
    # Listando os exercícios na tela
    for i, exercicio in enumerate(exercicios, 1):
        st.write(f"{i}. {exercicio}")
        
    # Rodapé do Relatório
    st.caption("Garantimos a segurança dos dados. IA desenvolvida para auxiliar a tomada de decisão dos instrutores.")
else:
    st.info("Adicione os dados na barra lateral esquerda e clique em 'Analisar e Gerar Plano' para rodar o sistema.")
