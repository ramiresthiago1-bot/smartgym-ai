import streamlit as st
import pandas as pd

st.set_page_config(page_title="SmartGym AI Pro", page_icon="🏋️‍♂️", layout="centered")

class Aluno:
    def __init__(self, nome, idade, peso, objetivo, frequencia_semanal, nivel_fadiga):
        self.nome = nome
        self.idade = idade
        self.peso = peso
        self.objetivo = objetivo
        self.frequencia_semanal = frequencia_semanal
        self.nivel_fadiga = nivel_fadiga

    def calcular_risco_evasao(self):
        """Método que calcula a probabilidade de o aluno abandonar a academia"""
        score_risco = 0
        if self.frequencia_semanal <= 2: 
            score_risco += 40
        elif self.frequencia_semanal == 3: 
            score_risco += 20
            
        if self.nivel_fadiga >= 4: 
            score_risco += 40
        elif self.nivel_fadiga == 3: 
            score_risco += 15
            
        if self.idade < 21 or self.idade > 60: 
            score_risco += 10

        return min(max(score_risco, 5), 95)

    def gerar_plano_treino(self):
        """Método que define a estratégia e os exercícios ideais para o aluno"""
        if self.nivel_fadiga >= 4:
            return {
                "tipo": "Treino Regenerativo e Mobilidade",
                "ajuste": "⚠️ **Adaptação Ativada:** Volume reduzido devido à alta fadiga reportada.",
                "exercicios": [
                    {"num": "01", "nome": "Esteira (Caminhada Leve)", "obs": "15 minutos em ritmo constante de recuperação."},
                    {"num": "02", "nome": "Alongamento Dinâmico de Membros Inferiores", "obs": "3 séries de 45 segundos para flexibilidade."},
                    {"num": "03", "nome": "Leg Press 45° (Carga Leve)", "obs": "3 séries de 12 repetições focando na cadência."},
                    {"num": "04", "nome": "Puxada Alta na Polia (Carga Moderada)", "obs": "3 séries de 10 repetições focadas na postura."}
                ]
            }
        
        if self.objetivo == "Hipertrofia (Ganho de Massa)":
            return {
                "tipo": "Foco em Volume de Carga (Hipertrofia)",
                "ajuste": "⚡ **Performance Máxima:** Organismo recuperado para cargas progressivas.",
                "exercicios": [
                    {"num": "01", "nome": "Agachamento Livre com Barra", "obs": "4 séries de 8 repetições (Aumentar carga progressivamente)."},
                    {"num": "02", "nome": "Supino Reto com Barra", "obs": "4 séries de 10 repetições (Manter controle na descida)."},
                    {"num": "03", "nome": "Remada Curvada com Barra", "obs": "4 séries de 10 repetições."},
                    {"num": "04", "nome": "Desenvolvimento com Halteres", "obs": "3 séries de 12 repetições."}
                ]
            }
        elif self.objetivo == "Emagrecimento":
            return {
                "tipo": "Circuito de Alta Intensidade (HIIT)",
                "ajuste": "⚡ **Performance Máxima:** Organismo recuperado para queima calórica.",
                "exercicios": [
                    {"num": "01", "nome": "Bicicleta Ergométrica (HIIT)", "obs": "15 minutos alternando 30s máximo / 30s leve."},
                    {"num": "02", "nome": "Afundo com Halteres", "obs": "3 séries de 15 repetições cada perna."},
                    {"num": "03", "nome": "Flexão de Braço no Solo", "obs": "3 séries até a falha mecânica."},
                    {"num": "04", "nome": "Burpees Completos", "obs": "3 séries de 10 repetições com menor descanso possível."}
                ]
            }
        else:
            return {
                "tipo": "Treino Funcional e Resistência Geral",
                "ajuste": "⚡ **Performance Máxima:** Equilíbrio e condicionamento físico geral.",
                "exercicios": [
                    {"num": "01", "nome": "Corrida em Esteira Ritmo Moderado", "obs": "10 minutos para ativação cardiorrespiratória."},
                    {"num": "02", "nome": "Agachamento Sumô com Kettlebell", "obs": "3 séries de 15 repetições."},
                    {"num": "03", "nome": "Puxada no Triângulo (Polia Alta)", "obs": "3 séries de 12 repetições."},
                    {"num": "04", "nome": "Elevação Lateral com Halteres", "obs": "3 séries de 15 repetições."}
                ]
            }

st.markdown("""
    <style>
    .main-title { font-size: 42px; font-weight: 800; color: #CCFF00; text-align: center; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 2px; }
    .sub-title { font-size: 16px; color: #A0AEC0; text-align: center; margin-bottom: 30px; }
    .exercise-card { background-color: #1E293B; border-left: 5px solid #CCFF00; padding: 15px; border-radius: 8px; margin-bottom: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
    .exercise-title { font-size: 18px; font-weight: 700; color: #F8FAFC; margin-bottom: 2px; }
    .status-badge { padding: 12px; border-radius: 8px; font-weight: bold; text-align: center; font-size: 18px; margin-bottom: 20px; }
    .badge-high { background-color: #991B1B; color: #FCA5A5; border: 1px solid #F87171; }
    .badge-med { background-color: #9A3412; color: #FED7AA; border: 1px solid #FB923C; }
    .badge-low { background-color: #065F46; color: #A7F3D0; border: 1px solid #34D399; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏋️‍♂️ SmartGym AI Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Modelagem POO para Prescrição de Treinos e Retenção</div>', unsafe_allow_html=True)

st.sidebar.markdown("### 📝 Cadastro do Membro")
nome_input = st.sidebar.text_input("Nome do Aluno", "João Silva")
idade_input = st.sidebar.slider("Idade", 16, 90, 30)
peso_input = st.sidebar.number_input("Peso Atual (kg)", min_value=40.0, max_value=200.0, value=75.0)
objetivo_input = st.sidebar.selectbox("Objetivo Principal", ["Hipertrofia (Ganho de Massa)", "Emagrecimento", "Condicionamento Físico", "Saúde/Qualidade de Vida"])
frequencia_input = st.sidebar.slider("Frequência Semanal (Dias)", 1, 7, 3)
fadiga_input = st.sidebar.slider("Nível de Fadiga Atual (1=Baixo, 5=Alto)", 1, 5, 2)

aluno_atual = Aluno(nome_input, idade_input, peso_input, objetivo_input, frequencia_input, fadiga_input)

porcentagem_risco = aluno_atual.calcular_risco_evasao()
treino_gerado = aluno_atual.gerar_plano_treino()

aba_analise, aba_treino = st.tabs(["📊 Análise de Risco & Churn", "💪 Prescrição de Treino"])

with aba_analise:
    st.markdown(f"### Relatório de Retenção: **{aluno_atual.nome}**")
    st.write("Análise estruturada utilizando objetos e atributos de comportamento.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Frequência Cadastrada", value=f"{aluno_atual.frequencia_semanal}x / semana")
    with col2:
        st.metric(label="Índice de Fadiga", value=f"{aluno_atual.nivel_fadiga} / 5")
    
    st.markdown("#### Probabilidade de Evasão (Risco de Churn)")
    st.progress(porcentagem_risco / 100)
    
    if porcentagem_risco >= 60:
        st.markdown(f'<div class="status-badge badge-high">⚠️ ALTO RISCO DE EVASÃO: {porcentagem_risco}%</div>', unsafe_allow_html=True)
    elif porcentagem_risco >= 30:
        st.markdown(f'<div class="status-badge badge-med">🟡 MÉDIO RISCO DE EVASÃO: {porcentagem_risco}%</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-badge badge-low">🟢 ALUNO RETIDO COM SUCESSO: {porcentagem_risco}%</div>', unsafe_allow_html=True)

with aba_treino:
    st.markdown(f"### Ficha de Treino Automatizada para **{aluno_atual.nome}**")
    st.write(f"**Método Aplicado:** {treino_gerado['tipo']}")
    st.caption(treino_gerado['ajuste'])
    st.markdown("---")
    
    for ex in treino_gerado['exercicios']:
        st.markdown(f"""
            <div class="exercise-card">
                <div class="exercise-title">{ex['num']}. {ex['nome']}</div>
                <div style="color: #94A3B8; font-size: 14px;">{ex['obs']}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div style="text-align: center; color: #64748B; font-size: 12px;">SmartGym AI Pro v2.0 - Arquitetura de Classes (POO) - Desenvolvido por Thiago Ramires.</div>', unsafe_allow_html=True)
