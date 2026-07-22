import streamlit as st
import pandas as pd
from supabase import create_client, Client

st.set_page_config(page_title="SmartGym AI Pro + Cloud DB", page_icon="🏋️‍♂️", layout="centered")

SUPABASE_URL = "https://jljusbugiwcmqknpalzk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpsanVzYnVnaXdjbXFrbnBhbHprIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQ3MzE1NTIsImV4cCI6MjEwMDMwNzU1Mn0.b8clTjzcq74Lky2qngno7_0Hl5osfrMT-WkZnvVHTDw"

@st.cache_resource
def inicializar_banco():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    supabase: Client = inicializar_banco()
except Exception as e:
    st.error("Erro ao conectar ao banco de dados na nuvem. Verifique suas credenciais.")

class Aluno:
    def __init__(self, nome, idade, peso, objetivo, frequencia_semanal, nivel_fadiga):
        self.nome = nome
        self.idade = idade
        self.peso = peso
        self.objetivo = objetivo
        self.frequencia_semanal = frequencia_semanal
        self.nivel_fadiga = nivel_fadiga

    def calcular_risco_evasao(self):
        score_risco = 0
        if self.frequencia_semanal <= 2: score_risco += 40
        elif self.frequencia_semanal == 3: score_risco += 20
        if self.nivel_fadiga >= 4: score_risco += 40
        elif self.nivel_fadiga == 3: score_risco += 15
        if self.idade < 21 or self.idade > 60: score_risco += 10
        return min(max(score_risco, 5), 95)

    def gerar_plano_treino(self):
        if self.nivel_fadiga >= 4:
            return {
                "tipo": "Treino Regenerativo e Mobilidade",
                "ajuste": "⚠️ **Adaptação Ativada:** Volume reduzido devido à alta fadiga reportada.",
                "exercicios": ["Esteira (Caminhada Leve) - 15 min", "Alongamento Dinâmico - 3x45s", "Leg Press 45° (Leve) - 3x12"]
            }
        if self.objetivo == "Hipertrofia (Ganho de Massa)":
            return {
                "tipo": "Foco em Volume de Carga (Hipertrofia)",
                "ajuste": "⚡ **Performance Máxima:** Cargas progressivas.",
                "exercicios": ["Agachamento Livre - 4x8", "Supino Reto - 4x10", "Remada Curvada - 4x10"]
            }
        return {
            "tipo": "Treino Geral",
            "ajuste": "⚡ Condicionamento Físico.",
            "exercicios": ["Corrida Moderada - 10 min", "Agachamento Sumô - 3x15", "Puxada Alta - 3x12"]
        }

st.markdown("""
    <style>
    .main-title { font-size: 42px; font-weight: 800; color: #CCFF00; text-align: center; margin-bottom: 5px; text-transform: uppercase; }
    .sub-title { font-size: 16px; color: #A0AEC0; text-align: center; margin-bottom: 30px; }
    .exercise-card { background-color: #1E293B; border-left: 5px solid #CCFF00; padding: 15px; border-radius: 8px; margin-bottom: 12px; }
    .status-badge { padding: 12px; border-radius: 8px; font-weight: bold; text-align: center; font-size: 18px; margin-bottom: 20px; }
    .badge-high { background-color: #991B1B; color: #FCA5A5; }
    .badge-low { background-color: #065F46; color: #A7F3D0; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏋️‍♂️ SmartGym AI Cloud</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Conexão com Banco de Dados PostgreSQL na Nuvem</div>', unsafe_allow_html=True)

st.sidebar.markdown("### 📝 Cadastro do Membro")
nome_input = st.sidebar.text_input("Nome do Aluno", "João Silva")
idade_input = st.sidebar.slider("Idade", 16, 90, 30)
peso_input = st.sidebar.number_input("Peso Atual (kg)", min_value=40.0, max_value=200.0, value=75.0)
objetivo_input = st.sidebar.selectbox("Objetivo Principal", ["Hipertrofia (Ganho de Massa)", "Emagrecimento", "Saúde/Qualidade de Vida"])
frequencia_input = st.sidebar.slider("Frequência Semanal (Dias)", 1, 7, 3)
fadiga_input = st.sidebar.slider("Nível de Fadiga Atual (1=Baixo, 5=Alto)", 1, 5, 2)

aba_cadastro, aba_historico = st.tabs(["📝 Avaliar Aluno", "🗂️ Histórico de Alunos Salvos"])

with aba_cadastro:
    if st.sidebar.button("💾 Analisar e Salvar na Nuvem"):
        aluno_atual = Aluno(nome_input, idade_input, peso_input, objetivo_input, frequencia_input, fadiga_input)
        risco = aluno_atual.calcular_risco_evasao()
        treino = aluno_atual.gerar_plano_treino()
        
        dados_aluno = {
            "nome": aluno_atual.nome,
            "idade": aluno_atual.idade,
            "peso": aluno_atual.peso,
            "objetivo": aluno_atual.objetivo,
            "frequencia": aluno_atual.frequencia_semanal,
            "fadiga": aluno_atual.nivel_fadiga,
            "risco_evasao": risco
        }
        
        try:
            supabase.table("alunos_smartgym").insert(dados_aluno).execute()
            st.success(f"🎉 Sucesso! Os dados de {aluno_atual.nome} foram salvos com segurança na nuvem.")
        except Exception as error:
            st.error(f"Erro ao salvar no banco de dados: {error}")
            
        st.markdown(f"### Plano de Treino para: **{aluno_atual.nome}**")
        st.write(f"Risco de Desistência calculado: **{risco}%**")
        for ex in treino['exercicios']:
            st.markdown(f'<div class="exercise-card">🔹 {ex}</div>', unsafe_allow_html=True)
    else:
        st.info("Preencha os dados na barra lateral e clique em 'Analisar e Salvar na Nuvem'.")

with aba_historico:
    st.markdown("### 📋 Alunos Cadastrados na Nuvem (PostgreSQL)")
    if st.button("🔄 Atualizar Lista da Nuvem"):
        try:
            resposta = supabase.table("alunos_smartgym").select("*").order("id", desc=True).execute()
            if resposta.data:
                df = pd.DataFrame(resposta.data)
                df.columns = ['ID', 'Nome', 'Idade', 'Peso (kg)', 'Objetivo', 'Dias/Semana', 'Fadiga', 'Risco Churn (%)', 'Data do Cadastro']
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Nenhum aluno cadastrado no banco de dados ainda.")
        except Exception as error:
            st.error(f"Erro ao buscar histórico: {error}")
