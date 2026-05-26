import streamlit as st
from datetime import datetime
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Justificativa de Ponto", page_icon="📝", layout="centered")

st.title("📝 Ajuste de Ponto Eletrônico")
st.markdown("Esqueceu de bater o ponto? Preencha os campos abaixo para enviar a justificativa.")
st.markdown("---")

# Formulário
with st.form(key="form_ponto", clear_on_submit=True):
    colaborador = st.selectbox("Selecione seu nome:", ["Selecione...", "Lucas Silva", "Mariana Costa"])
    tipo_trabalho = st.radio("Regime de trabalho no dia:", ["Interno", "Externo"], horizontal=True)
    data_esquecimento = st.date_input("Data do ponto esquecido:", datetime.today())
    
    st.markdown("**Qual marcação você esqueceu?**")
    col1, col2 = st.columns(2)
    with col1:
        tipo_marcacao = st.selectbox("Período:", ["Entrada", "Saída", "Almoço (Ida)", "Almoço (Volta)"])
    with col2:
        hora_correta = st.time_input("Horário correto da marcação:", value=datetime.now().time())

    justificativa = st.text_area("Motivo do esquecimento / Observações:", placeholder="Ex: Cliente externo...")

    botao_enviar = st.form_submit_button(label="Enviar Justificativa")

# Processamento do envio
if botao_enviar:
    if colaborador == "Selecione...":
        st.error("Por favor, selecione o seu nome antes de enviar.")
    else:
        with st.spinner("Processando sua justificativa..."):
            # Monta o dicionário com os dados organizados
            dados_envio = {
                "Data do Envio": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "Colaborador": colaborador,
                "Regime": tipo_trabalho,
                "Data do Esquecimento": data_esquecimento.strftime("%d/%m/%Y"),
                "O que esqueceu": tipo_marcacao,
                "Horário Correto": hora_correta.strftime("%H:%M"),
                "Justificativa": justificativa
            }
            
            # Mensagem de Sucesso Visual com os dados confirmados
            st.success(f"🎉 Obrigado, {colaborador}! Justificativa registrada com sucesso!")
            
            # Mostra um recibo bonito na tela para o funcionário
            st.info("### 📋 Recibo da Solicitação")
            df_recibo = pd.DataFrame([dados_envio])
            st.dataframe(df_recibo, hide_index=True)
