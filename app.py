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
    def __init__(self, nome, idade, peso, sexo, nivel, objetivo, frequencia_semanal, nivel_fadiga):
        self.nome = nome
        self.idade = idade
        self.peso = peso
        self.sexo = sexo
        self.nivel = nivel
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
                "tipo": f"Regenerativo e Mobilidade ({self.nivel})",
                "ajuste": "⚠️ **Volume Reduzido:** Foco em recuperação articular e muscular geral.",
                "exercicios": ["Esteira (Caminhada Leve) - 15 min", "Alongamento Dinâmico Geral - 3x45s", "Mobilidade de Quadril e Tornozelos"]
            }
        
        if self.objetivo == "Hipertrofia (Ganho de Massa)":
            if self.sexo == "Masculino":
                if self.nivel == "Iniciante":
                    return {"tipo": "Hipertrofia Masculina - Adaptação Anatomica", "ajuste": "🌱 Foco em aprender a execução e consistência.", "exercicios": ["Supino na Máquina - 3x12", "Puxada Alta - 3x12", "Leg Press 45° - 3x10", "Rosca Direta com Halteres - 3x12"]}
                elif self.nivel == "Intermediário":
                    return {"tipo": "Hipertrofia Masculina - ABC Intermediário", "ajuste": "⚡ Foco em progressão moderada de carga.", "exercicios": ["Supino Reto com Barra - 4x10", "Remada Curvada - 4x10", "Desenvolvimento Halteres - 3x12", "Agachamento Livre - 4x8"]}
                else:
                    return {"tipo": "Hipertrofia Masculina - Avançado (GVT/FST-7)", "ajuste": "🔥 Alta intensidade, técnicas avançadas e drop-sets.", "exercicios": ["Supino Inclinado com Halteres + Crucifixo - 4x8+10", "Remada Cavalinho (Drop-set na última) - 4x10", "Agachamento Livre com Barra (Carga Máxima) - 4x6", "Rosca 21 na Barra W - 3x"]}
            else:
                if self.nivel == "Iniciante":
                    return {"tipo": "Hipertrofia Feminina - Adaptação Geral", "ajuste": "🌱 Foco em ativação muscular básica.", "exercicios": ["Cadeira Extensora - 3x12", "Cadeira Flexora - 3x12", "Puxada Alta - 3x12", "Agachamento com Peso Corporal - 3x15"]}
                elif self.nivel == "Intermediário":
                    return {"tipo": "Hipertrofia Feminina - Foco Inferiores", "ajuste": "⚡ Foco em volume e desenho muscular.", "exercicios": ["Agachamento Livre - 4x10", "Elevação Pélvica - 4x12", "Leg Press Horizonal - 3x12", "Stiff com Halteres - 4x10"]}
                else:
                    return {"tipo": "Hipertrofia Feminina - Avançado (Membros Inferiores)", "ajuste": "🔥 Estímulo tensional máximo e falha concêntrica.", "exercicios": ["Agachamento Livre com Barra - 4x6 (Pesado)", "Elevação Pélvica (Rest-Pause) - 4x10", "Cadeira Extensora (Isometria de 3s no topo) - 3x10", "Afundo Reverso no Smith - 4x8"]}
                
        elif self.objetivo == "Emagrecimento":
            if self.nivel == "Iniciante":
                return {"tipo": "Cardio Adaptativo", "ajuste": "🌱 Ritmo constante e sem impacto severo.", "exercicios": ["Caminhada na Esteira Inclinada - 20 min", "Bicicleta Ergométrica - 15 min", "Abdominal Infra - 3x15"]}
            elif self.nivel == "Intermediário":
                return {"tipo": "Circuito Funcional Metábolico", "ajuste": "⚡ Alternando exercícios de força e cardio.", "exercicios": ["HIIT na Bicicleta - 15 min (30s forte/30s leve)", "Agachamento Sumô + Polichinelos - 3x15", "Flexão de Braço + Prancha - 3x45s"]}
            else: 
                return {"tipo": "Protocolo Tabata / Cross-Training", "ajuste": "🔥 Intensidade máxima e zonas de queima de gordura elevadas.", "exercicios": ["Corrida na Esteira (HIIT Máximo) - 15 min", "Burpees Completos - 4x12", "Agachamento Salto (Jump Squat) - 4x20", "Abdominal Remador - 4x25"]}

        return {
            "tipo": f"Condicionamento Físico Geral ({self.nivel})",
            "ajuste": "⚡ Equilíbrio, saúde e bem-estar geral.",
            "exercicios": ["Caminhada/Corrida Leve - 15 min", "Agachamento Livre - 3x12", "Remada Sentada na Polia - 3x12", "Prancha Isométrica - 3x30s"]
        }

st.markdown("""
    <style>
    .main-title { font-size: 42px; font-weight: 800; color: #CCFF00; text-align: center; margin-bottom: 5px; text-transform: uppercase; }
    .sub-title { font-size: 16px; color: #A0AEC0; text-align: center; margin-bottom: 30px; }
    .exercise-card { background-color: #1E293B; border-left: 5px solid #CCFF00; padding: 15px; border-radius: 8px; margin-bottom: 12px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏋️‍♂️ SmartGym AI Cloud</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Prescrição Ultra Inteligente por Gênero, Objetivo e Experiência</div>', unsafe_allow_html=True)

st.sidebar.markdown("### 📝 Cadastro do Membro")
nome_input = st.sidebar.text_input("Nome do Aluno", "João Silva")
idade_input = st.sidebar.slider("Idade", 16, 90, 30)
peso_input = st.sidebar.number_input("Peso Atual (kg)", min_value=40.0, max_value=200.0, value=75.0)

sexo_input = st.sidebar.radio("Sexo Biológico", ["Masculino", "Feminino"])

nivel_input = st.sidebar.selectbox("Nível de Experiência", ["Iniciante", "Intermediário", "Avançado"])

objetivo_input = st.sidebar.selectbox("Objetivo Principal", ["Hipertrofia (Ganho de Massa)", "Emagrecimento", "Saúde/Qualidade de Vida"])
frequencia_input = st.sidebar.slider("Frequência Semanal (Dias)", 1, 7, 3)
fadiga_input = st.sidebar.slider("Nível de Fadiga Atual (1=Baixo, 5=Alto)", 1, 5, 2)

aba_cadastro, aba_historico = st.tabs(["📝 Avaliar Aluno", "🗂️ Histórico de Alunos Salvos"])

with aba_cadastro:
    if st.sidebar.button("💾 Analisar e Salvar na Nuvem"):
        aluno_atual = Aluno(nome_input, idade_input, peso_input, sexo_input, nivel_input, objetivo_input, frequencia_input, fadiga_input)
        risco = aluno_atual.calcular_risco_evasao()
        treino = aluno_atual.gerar_plano_treino()
        
        dados_aluno = {
            "nome": aluno_atual.nome,
            "idade": aluno_atual.idade,
            "peso": aluno_atual.peso,
            "sexo": aluno_atual.sexo,
            "nivel": aluno_atual.nivel,
            "objetivo": aluno_atual.objetivo,
            "frequencia": aluno_atual.frequencia_semanal,
            "fadiga": aluno_atual.nivel_fadiga,
            "risco_evasao": risco
        }
        
        try:
            supabase.table("alunos_smartgym").insert(dados_aluno).execute()
            st.success(f"🎉 Sucesso! Os dados de {aluno_atual.nome} foram salvos com segurança na nuvem.")
        except:
            try:
                if "nivel" in dados_aluno: del dados_aluno["nivel"]
                if "sexo" in dados_aluno: del dados_aluno["sexo"]
                supabase.table("alunos_smartgym").insert(dados_aluno).execute()
                st.success(f"🎉 Salvo na nuvem!")
            except Exception as error:
                st.error(f"Erro no banco: {error}")
            
        st.markdown(f"### Plano de Treino para: **{aluno_atual.nome}**")
        st.write(f"Perfil: **{aluno_atual.sexo} | {aluno_atual.nivel} | Risco de Churn: {risco}%**")
        st.write(f"🎯 **Treino Recomendado:** {treino['tipo']}")
        st.caption(treino['ajuste'])
        st.markdown("---")
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

