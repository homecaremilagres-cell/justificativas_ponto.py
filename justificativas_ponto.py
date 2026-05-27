import streamlit as st
from datetime import datetime
import requests
import json

# Configuração da página
st.set_page_config(page_title="Justificativa de Ponto", page_icon="📝", layout="centered")

st.title("📝 Ajuste de Ponto Eletrônico")
st.markdown("Esqueceu de bater o ponto? Preencha os campos abaixo para enviar a justificativa.")
st.markdown("---")

# URL do seu Apps Script
URL_WEBAPP = "https://script.google.com/macros/s/AKfycbzl_CLpkDt0j-HNSpp5XEpVPDz2tss_i56p-uiJ-D8CRjL-D23AxDWkM2DMS2HJld0c/exec"

# Formulário na tela
with st.form(key="form_ponto", clear_on_submit=True):
    colaborador = st.selectbox("Selecione seu nome:", ["Selecione...", "Lucas Silva", "Mariana Costa", "HOME CARE MILAGRES", "Arthur Gonçalves de Siqueira", "João Gabriel da Silva"])
    tipo_trabalho = st.radio("Regime de trabalho no dia:", ["Interno", "Externo"], horizontal=True)
    data_esquecimento = st.date_input("Data do ponto esquecido:", datetime.today())
    
    st.markdown("**Qual marcação você esqueceu?**")
    col1, col2 = st.columns(2)
    with col1:
        tipo_marcacao = st.selectbox("Período:", ["Entrada", "Saída", "Almoço (Ida)", "Almoço (Volta)"])
    with col2:
        # Usamos o parâmetro key para fixar o valor no estado do formulário
        st.time_input("Horário correto da marcação:", value=datetime.now().time(), key="valor_hora_digitado")

    justificativa = st.text_area("Motivo do esquecimento / Observações:", placeholder="Ex: Cliente externo...")

    botao_enviar = st.form_submit_button(label="Enviar Justificativa")

# Processamento do envio
if botao_enviar:
    if colaborador == "Selecione...":
        st.error("Por favor, selecione o seu nome antes de enviar.")
    else:
        with st.spinner("Enviando justificativa... Por favor, aguarde."):
            
            # Resgatamos a hora diretamente do estado do formulário antes que ele limpe a tela
            hora_selecionada = st.session_state.valor_hora_digitado
            
            payload = {
                "data_envio": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "colaborador": colaborador,
                "regime": tipo_trabalho,
                "data_esquecimento": data_esquecimento.strftime("%d/%m/%Y"),
                "tipo_marcacao": tipo_marcacao,
                "hora_correta": hora_selecionada.strftime("%H:%M"),  # 👈 Agora o Python lê o valor real alterado
                "justificativa": justificativa
            }
            
            try:
                resposta = requests.post(URL_WEBAPP, data=json.dumps(payload), headers={"Content-Type": "application/json"})
                if resposta.status_code == 200 or "Sucesso" in resposta.text:
                    st.success(f"🎉 Sucesso! Sua justificativa foi enviada direto para o RH!")
                else:
                    st.error("Ops! O servidor do Google recebeu os dados mas não conseguiu salvar.")
            except Exception as e:
                st.error(f"Erro ao conectar com o Google: {e}")
