import streamlit as st
import pandas as pd
from supabase import create_client, Client

st.set_page_config(page_title="SmartGym AI Pro + Cloud DB", page_icon="🏋️‍♂️", layout="centered")

SUPABASE_URL = "https://supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpsanVzYnVnaXdjbXFrbnBhbHprIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQ3MzE1NTIsImV4cCI6MjEwMDMwNzU1Mn0.b8clTjzcq74Lky2qngno7_0Hl5osfrMT-WkZnvVHTDw"

@st.cache_resource
def inicializar_banco():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    supabase: Client = inicializar_banco()
except Exception as e:
    st.error("Erro ao conectar ao banco de dados na nuvem.")

class Aluno:
    def __init__(self, nome, idade, peso, sexo, objetivo, frequencia_semanal, nivel_fadiga):
        self.nome = nome
        self.idade = idade
        self.peso = peso
        self.sexo = sexo 
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
                "ajuste": "⚠️ **Volume Reduzido:** Foco em recuperação muscular geral.",
                "exercicios": ["Esteira (Caminhada Leve) - 15 min", "Alongamento Dinâmico - 3x45s", "Leg Press 45° (Leve) - 3x12"]
            }
        
        if self.objetivo == "Hipertrofia (Ganho de Massa)":
            if self.sexo == "Masculino":
                return {
                    "tipo": "Hipertrofia - Foco em Membros Superiores (Masculino)",
                    "ajuste": "⚡ **Performance:** Estímulo focado em braços, peito e costas.",
                    "exercicios": ["Supino Reto com Barra - 4x10", "Remada Curvada - 4x10", "Desenvolvimento Halteres - 3x12", "Agachamento Livre - 4x8"]
                }
            else:
                return {
                    "tipo": "Hipertrofia - Foco em Membros Inferiores (Feminino)",
                    "ajuste": "⚡ **Performance:** Estímulo focado em quadríceps, glúteos e posterior.",
                    "exercicios": ["Agachamento Livre - 4x10", "Elevação Pélvica na Máquina - 4x12", "Cadeira Extensora - 3x15", "Puxada Alta (Costas) - 3x10"]
                }
                
        elif self.objetivo == "Emagrecimento":
            return {
                "tipo": "Circuito Cardiorrespiratório Integrado",
                "ajuste": "⚡ **Alta Intensidade:** Queima calórica otimizada.",
                "exercicios": ["Corrida Intervalada - 15 min", "Afundo com Halteres - 3x15", "Flexão ou Prancha - 3x45s"]
            }
            
        return {
            "tipo": "Treino Geral de Condicionamento",
            "ajuste": "⚡ Manutenção de saúde e resistência.",
            "exercicios": ["Bicicleta - 10 min", "Agachamento Sumô - 3x15", "Puxada na Polia - 3x12"]
        }

st.markdown("""
    <style>
    .main-title { font-size: 42px; font-weight: 800; color: #CCFF00; text-align: center; margin-bottom: 5px; text-transform: uppercase; }
    .sub-title { font-size: 16px; color: #A0AEC0; text-align: center; margin-bottom: 30px; }
    .exercise-card { background-color: #1E293B; border-left: 5px solid #CCFF00; padding: 15px; border-radius: 8px; margin-bottom: 12px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏋️‍♂️ SmartGym AI Cloud</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Prescrição Inteligente Segmentada por Gênero e Objetivo</div>', unsafe_allow_html=True)

st.sidebar.markdown("### 📝 Cadastro do Membro")
nome_input = st.sidebar.text_input("Nome do Aluno", "João Silva")
idade_input = st.sidebar.slider("Idade", 16, 90, 30)
peso_input = st.sidebar.number_input("Peso Atual (kg)", min_value=40.0, max_value=200.0, value=75.0)

sexo_input = st.sidebar.radio("Sexo Biológico", ["Masculino", "Feminino"])

objetivo_input = st.sidebar.selectbox("Objetivo Principal", ["Hipertrofia (Ganho de Massa)", "Emagrecimento", "Saúde/Qualidade de Vida"])
frequencia_input = st.sidebar.slider("Frequência Semanal (Dias)", 1, 7, 3)
fadiga_input = st.sidebar.slider("Nível de Fadiga Atual (1=Baixo, 5=Alto)", 1, 5, 2)

aba_cadastro, aba_historico = st.tabs(["📝 Avaliar Aluno", "🗂️ Histórico de Alunos Salvos"])

with aba_cadastro:
    if st.sidebar.button("💾 Analisar e Salvar na Nuvem"):
        aluno_atual = Aluno(nome_input, idade_input, peso_input, sexo_input, objetivo_input, frequencia_input, fadiga_input)
        risco = aluno_atual.calcular_risco_evasao()
        treino = aluno_atual.gerar_plano_treino()
        
        dados_aluno = {
            "nome": aluno_atual.nome,
            "idade": aluno_atual.idade,
            "peso": aluno_atual.peso,
            "sexo": aluno_atual.sexo,
            "objetivo": aluno_atual.objetivo,
            "frequencia": aluno_atual.frequencia_semanal,
            "fadiga": aluno_atual.nivel_fadiga,
            "risco_evasao": risco
        }
        
        try:
            supabase.table("alunos_smartgym").insert(dados_aluno).execute()
            st.success(f"🎉 Sucesso! Os dados de {aluno_atual.nome} foram salvos com segurança na nuvem.")
        except Exception as error:
            try:
                del dados_aluno["sexo"]
                supabase.table("alunos_smartgym").insert(dados_aluno).execute()
                st.success(f"🎉 Salvo na nuvem (sem coluna sexo).")
            except:
                st.error(f"Erro no banco: {error}")
            
        st.markdown(f"### Plano de Treino para: **{aluno_atual.nome}** ({aluno_atual.sexo})")
        st.write(f"Risco de Desistência calculado: **{risco}%**")
        st.write(f"**Treino Recomendado:** {treino['tipo']}")
        for ex in treino['exercicios']:
            st.markdown(f'<div class="exercise-card">🔹 {ex}</div>', unsafe_allow_html=True)
    else:
        st.info("Preencha os dados na barra lateral e clique em 'Analisar e Salvar na Nuvem'.")

with aba_historico:
    st.markdown("### 📋 Alunos Cadastrados na Nuvem")
    if st.button("🔄 Atualizar Lista da Nuvem"):
        try:
            resposta = supabase.table("alunos_smartgym").select("*").order("id", desc=True).execute()
            if resposta.data:
                df = pd.DataFrame(resposta.data)
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Nenhum aluno cadastrado ainda.")
        except Exception as error:
            st.error(f"Erro ao buscar histórico: {error}")
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #64748B; font-size: 14px; font-weight: 500; margin-top: 20px;">
        🚀 SmartGym AI Cloud v3.0 | Desenvolvido com ❤️ por 
        <a href="https://github.com" target="_blank" style="color: #CCFF00; text-decoration: none; font-weight: bold;">
            Thiago Ramires
        </a>
    </div>
""", unsafe_allow_html=True)
