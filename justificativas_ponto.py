import streamlit as st
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Justificativa de Ponto", page_icon="📝", layout="centered")

st.title("📝 Ajuste de Ponto Eletrônico")
st.markdown("Esqueceu de bater o ponto? Preencha os campos abaixo.")
st.markdown("---")

# Formulário visual limpo
with st.form(key="form_ponto", clear_on_submit=True):
    colaborador = st.selectbox("Selecione seu nome:", ["Selecione...", "Lucas Silva", "Mariana Costa"])
    tipo_trabalho = st.radio("Regime de trabalho no dia:", ["Interno", "Externo"], horizontal=True)
    data_esquecimento = st.date_input("Data do ponto esquecido:", datetime.today())
    tipo_marcacao = st.selectbox("Período:", ["Entrada", "Saída", "Almoço (Ida)", "Almoço (Volta)"])
    justificativa = st.text_area("Motivo do esquecimento / Observações:")
    
    botao_enviar = st.form_submit_button(label="Enviar Justificativa")

if botao_enviar:
    st.success(f"Formulário funcionando! Olá {colaborador}, sua estrutura visual está pronta!")
