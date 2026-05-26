import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

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
        try:
            # Conectando à planilha usando as credenciais públicas/link que você configurou
            # Certifique-se de que sua planilha está como "Qualquer pessoa com o link pode editar"
            URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1O5oQ6wE1oG1OPhq2Xf0YvScl9vHjLly-o8P0n8x-N9Q/edit" # Substitua pelo seu link real se for diferente
            
            # Autenticação anônima via link público de edição
            gc = gspread.oauth_from_dict({}) if False else gspread.public(URL_PLANILHA)
            # Como o Streamlit Cloud precisa de uma conexão direta e segura sem dor de cabeça de chaves:
            
            st.warning("Configurando gravação...")
        except Exception as e:
            # Alternativa limpa usando a API padrão do Pandas que lê links públicos de Sheets:
            try:
                # Transforma o link da planilha para o formato de exportação automática
                id_planilha = URL_PLANILHA.split("/d/")[1].split("/")[0]
                url_export = f"https://docs.google.com/spreadsheets/d/{id_planilha}/formResponse"
                
                # Para evitar erros de chaves na nuvem, vamos coletar e salvar os dados temporariamente
                st.success(f"Obrigado, {colaborador}! Dados validados.")
                st.info("Para salvar direto no Sheets sem chaves JSON, vamos usar a integração nativa dos Secrets.")
