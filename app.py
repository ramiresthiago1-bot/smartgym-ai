import streamlit as st
import pandas as pd

# CONFIGURAÇÃO DA PÁGINA (Interface limpa e profissional)
st.set_page_config(page_title="SmartGym AI", page_icon="🏋️‍♂️", layout="centered")

# --- ESTILIZAÇÃO CSS CUSTOMIZADA (Visual Premium / Dark Mode Fitness) ---
st.markdown("""
    <style>
    /* Estilo global de fontes e fundos */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #CCFF00; /* Amarelo Neon Fitness */
        text-align: center;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .sub-title {
        font-size: 16px;
        color: #A0AEC0;
        text-align: center;
        margin-bottom: 30px;
    }
    /* Estilização dos Cards de Exercícios */
    .exercise-card {
        background-color: #1E293B;
        border-left: 5px solid #CCFF00;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .exercise-title {
        font-size: 18px;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 2px;
    }
    /* Alertas customizados de Risco */
    .status-badge {
        padding: 12px;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        font-size: 18px;
        margin-bottom: 20px;
    }
    .badge-high { background-color: #991B1B; color: #FCA5A5; border: 1px solid #F87171; }
    .badge-med { background-color: #9A3412; color: #FED7AA; border: 1px solid #FB923C; }
    .badge-low { background-color: #065F46; color: #A7F3D0; border: 1px solid #34D399; }
    </style>
""", unsafe_allow_html=True)

# CABEÇALHO DO APLICATIVO
st.markdown('<div class="main-title">🏋️‍♂️ SmartGym AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Inteligência Artificial para Prescrição de Treinos e Retenção de Alunos</div>', unsafe_allow_html=True)

# --- SIDEBAR: ENTRADA DE DADOS ---
st.sidebar.markdown("### 📝 Dados do Membro")
nome = st.sidebar.text_input("Nome do Aluno", "João Silva")
idade = st.sidebar.slider("Idade", 16, 90, 30)
peso = st.sidebar.number_input("Peso Atual (kg)", min_value=40.0, max_value=200.0, value=75.0)

objetivo = st.sidebar.selectbox(
    "Objetivo Principal", 
    ["Hipertrofia (Ganho de Massa)", "Emagrecimento", "Condicionamento Físico", "Saúde/Qualidade de Vida"]
)

frequencia_semanal = st.sidebar.slider("Frequência Semanal (Dias)", 1, 7, 3)
nivel_fadiga = st.sidebar.slider("Nível de Fadiga Atual (1=Baixo, 5=Alto)", 1, 5, 2)

# --- FLUXO PRINCIPAL ---
# Criamos duas abas para separar a análise gráfica das tabelas de exercícios
aba_analise, aba_treino = st.tabs(["📊 Análise de Risco & Churn", "💪 Prescrição de Treino"])

# 1. CÁCULO DE LOGICA DE NEGÓCIO (Independente da Aba)
score_risco = 0
if frequencia_semanal <= 2: score_risco += 40
elif frequencia_semanal == 3: score_risco += 20
if nivel_fadiga >= 4: score_risco += 40
elif nivel_fadiga == 3: score_risco += 15
if idade < 21 or idade > 60: score_risco += 10

porcentagem_risco = min(max(score_risco, 5), 95)

# --- CONTEÚDO DA ABA 1: ANÁLISE DE RISCO ---
with aba_analise:
    st.markdown(f"### Relatório de Retenção: **{nome}**")
    st.write("Métricas calculadas em tempo real com base no padrão comportamental e de frequência.")
    
    # Grid de Indicadores Visuais
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Frequência Alvo", value=f"{frequencia_semanal}x / semana")
    with col2:
        st.metric(label="Índice de Fadiga", value=f"{nivel_fadiga} / 5", delta="- Estável" if nivel_fadiga < 3 else "+ Alerta", delta_color="inverse")
    
    st.markdown("#### Probabilidade de Evasão (Risco de Churn)")
    
    # Barra de progresso nativa do Streamlit
    st.progress(porcentagem_risco / 100)
    
    # Badge Dinâmico Customizado via HTML/CSS
    if porcentagem_risco >= 60:
        st.markdown(f'<div class="status-badge badge-high">⚠️ ALTO RISCO DE EVASÃO: {porcentagem_risco}%</div>', unsafe_allow_html=True)
        st.error("💡 **Ação recomendada**: Entre em contato imediatamente com o aluno para ajustar o plano de horários ou oferecer suporte motivacional.")
    elif porcentagem_risco >= 30:
        st.markdown(f'<div class="status-badge badge-med">🟡 MÉDIO RISCO DE EVASÃO: {porcentagem_risco}%</div>', unsafe_allow_html=True)
        st.warning("💡 **Ação recomendada**: Agende uma reavaliação física e verifique se as cargas estão adequadas.")
    else:
        st.markdown(f'<div class="status-badge badge-low">🟢 ALUNO RETIDO COM SUCESSO: {porcentagem_risco}%</div>', unsafe_allow_html=True)
        st.success("💡 **Ação recomendada**: Aluno altamente engajado. Mantenha o acompanhamento padrão e parabenize a consistência.")

# --- CONTEÚDO DA ABA 2: PRESCRIÇÃO DE TREINO ---
with aba_treino:
    st.markdown(f"### Ficha de Treino Automatizada para **{nome}**")
    
    # Determinação do treino com base na fadiga e objetivo
    if nivel_fadiga >= 4:
        tipo_treino = "Treino Regenerativo e Mobilidade"
        ajuste_fadiga = "⚠️ **Adaptação Ativada:** Volume reduzido devido à alta fadiga reportada."
        exercicios = [
            {"num": "01", "nome": "Esteira (Caminhada Leve)", "obs": "15 minutos em ritmo constante de recuperação."},
            {"num": "02", "nome": "Alongamento Dinâmico de Membros Inferiores", "obs": "3 séries de 45 segundos para flexibilidade."},
            {"num": "03", "nome": "Leg Press 45° (Carga Leve)", "obs": "3 séries de 12 repetições focando na cadência."},
            {"num": "04", "nome": "Puxada Alta na Polia (Carga Moderada)", "obs": "3 séries de 10 repetições focadas na postura."}
        ]
    else:
        ajuste_fadiga = "⚡ **Performance Máxima:** Organismo recuperado para cargas progressivas."
        if objetivo == "Hipertrofia (Ganho de Massa)":
            tipo_treino = "Foco em Volume de Carga (Hipertrofia)"
            exercicios = [
                {"num": "01", "nome": "Agachamento Livre com Barra", "obs": "4 séries de 8 repetições (Aumentar carga progressivamente)."},
                {"num": "02", "nome": "Supino Reto com Barra", "obs": "4 séries de 10 repetições (Manter controle na descida)."},
                {"num": "03", "nome": "Remada Curvada com Barra", "obs": "4 séries de 10 repetições."},
                {"num": "04", "nome": "Desenvolvimento com Halteres", "obs": "3 séries de 12 repetições."}
            ]
        elif objetivo == "Emagrecimento":
            tipo_treino = "Circuito de Alta Intensidade (HIIT)"
            exercicios = [
                {"num": "01", "nome": "Bicicleta Ergométrica (HIIT)", "obs": "15 minutos alternando 30s máximo / 30s leve."},
                {"num": "02", "nome": "Afundo com Halteres", "obs": "3 séries de 15 repetições cada perna."},
                {"num": "03", "nome": "Flexão de Braço no Solo", "obs": "3 séries até a falha mecânica."},
                {"num": "04", "nome": "Burpees Completos", "obs": "3 séries de 10 repetições com menor descanso possível."}
            ]
        else:
            tipo_treino = "Treino Funcional e Resistência Geral"
            exercicios = [
                {"num": "01", "nome": "Corrida em Esteira Ritmo Moderado", "obs": "10 minutos para ativação cardiorrespiratória."},
                {"num": "02", "nome": "Agachamento Sumô com Kettlebell", "obs": "3 séries de 15 repetições."},
                {"num": "03", "nome": "Puxada no Triângulo (Polia Alta)", "obs": "3 séries de 12 repetições."},
                {"num": "04", "nome": "Elevação Lateral com Halteres", "obs": "3 séries de 15 repetições."}
            ]
            
    st.write(f"**Método Aplicado:** {tipo_treino}")
    st.caption(ajuste_fadiga)
    st.markdown("---")
    
    # Gerando os Cards de Exercício dinamicamente usando CSS customizado
    for ex in exercicios:
        st.markdown(f"""
            <div class="exercise-card">
                <div class="exercise-title">{ex['num']}. {ex['nome']}</div>
                <div style="color: #94A3B8; font-size: 14px;">{ex['obs']}</div>
            </div>
        """, unsafe_allow_html=True)

# RODAPÉ DO APP
st.markdown("---")
st.markdown('<div style="text-align: center; color: #64748B; font-size: 12px;">SmartGym AI © 2026 - Desenvolvido por Thiago Ramires. Plataforma em conformidade com as diretrizes de ética em dados.</div>', unsafe_allow_html=True)
