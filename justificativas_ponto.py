import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# Configuração da página
st.set_page_config(page_title="Justificativa de Ponto", page_icon="📝", layout="centered")

st.title("📝 Ajuste de Ponto Eletrônico")
st.markdown("Esqueceu de bater o ponto? Preencha os campos abaixo para enviar a justificativa.")
st.markdown("---")

# Link da sua planilha do Google
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1J5lpTGO37379tCtfQ9Pdkdvu3ts1gQ89RvceCdZqe4Y/edit?usp=sharing"

# Criando a conexão com o Google Sheets de forma direta
conn = st.connection("gsheets", type=GSheetsConnection)

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
        with st.spinner("Enviando justificativa... Por favor, aguarde."):
            try:
                # 1. Lê os dados que já existem na planilha
                try:
                    dados_existentes = conn.read(ttl=0)
                except Exception:
                    dados_existentes = pd.DataFrame()

                # 2. Cria o novo registro com as colunas certinhas da sua planilha
                novo_registro = pd.DataFrame([{
                    "Data do Envio": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "Colaborador": colaborador,
                    "Regime": tipo_trabalho,
                    "Data do Esquecimento": data_esquecimento.strftime("%d/%m/%Y"),
                    "O que esqueceu": tipo_marcacao,
                    "Horário Correto": hora_correta.strftime("%H:%M"),
                    "Justificativa": justificativa
                }])
                
                # 3. Junta o novo registro com os antigos
                df_atualizado = pd.concat([dados_existentes, novo_registro], ignore_index=True)
                
                # 4. Salva de volta na planilha do Google
                conn.update(data=df_atualizado)
                
                st.success(f"Obrigado, {colaborador}! Sua justificativa foi enviada direto para a planilha do RH.")
            except Exception as erro:
                st.error("Ops! Ocorreu um problema ao salvar os dados.")
                st.info("Garanta que sua planilha está configurada no Google como: 'Qualquer pessoa com o link pode editar'.")
