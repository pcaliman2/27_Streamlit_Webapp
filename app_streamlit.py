import streamlit as st
import pandas as pd 
import os
import base64
import joblib

st.set_page_config(page_title="Predictor de MOS WCDMA", page_icon="📡")

modelopredictor = joblib.load("modelo_randon_forest_200_10_5_2.pkl")

# Verifica si la imagen existe
image_path = os.path.join(os.path.dirname(__file__), "mos3g.jpg")
if not os.path.exists(image_path):
    st.error(f"")
else:
    st.write(f"")

# Convierte la imagen a base64
try:
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    image_url = f"data:image/jpeg;base64,{encoded_image}"
except Exception as e:
    image_url = "https://via.placeholder.com/600x400"  # Imagen de respaldo
    st.error(f"Error al cargar la imagen: {e}")

# Inyecta CSS personalizado
st.markdown(
    f"""
    <style>
    /* Estilo para el contenedor principal */
    .stApp {{
        background-image: url("{image_url}");
        background-size: contain; /* Cambiado de cover a contain */
        background-position: center;
        background-repeat: no-repeat;
        max-width: 600px;
        margin: 50px auto;
        background-color: #cc6600; 
        padding: 30px;
        border-radius: 25px;
        box-shadow: 0px 0px 20px rgba(0,0,0,0.15);
        color: #0000cc;
    }}

  h1 {{
        text-align: center;
        color: #ff0000;
        margin-bottom: 30px;
    }}
    h6 {{
        text-align: left;
        margin-top: 30px;
        padding: 15px;
        border-radius: 10px;
        color: #ff00ff;
    }}
    /* Estilo para el contenedor del botón */
    div[data-testid="stButton"] {{
        background-color: transparent !important;
    }}

    /* Estilo base para el botón */
    div[data-testid="stButton"] > button {{
        background-color: #f0f0f0 !important; /* Gris inicial */
        color: black !important;
        border: 1px solid #000 !important;
        opacity: 1 !important;
        transition: all 0.2s ease !important;
    }}

    /* Estilo para el botón en hover */
    div[data-testid="stButton"] > button:hover {{
        background-color: #00ff00 !important; /* Verde en hover */
        color: black !important;
        border: 1px solid #000 !important;
        opacity: 1 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Título
st.markdown("<h1>Predictor de MOS WCDMA</h1>", unsafe_allow_html=True)

# Formulario
with st.form(key="mos_predictor_form"):
    # RSCP
    st.markdown("<h6>📶 RSCP (Received Signal Code Power) [-130 dBm (Malo) a -50 dBm</h6>", unsafe_allow_html=True)
    rsrp = st.number_input(
        "",
        min_value=-130.0,
        max_value=-50.0,
        step=0.1,
        format="%.1f",
        help="Rango: -130 dBm (Malo) a -50 dBm (Excelente)",
         label_visibility="collapsed" 
    )

    st.markdown("<h6>📡 ECIO (Energy per Chip to Interference) [-30 (Malo) a 0 (Excelente)]</h6>", unsafe_allow_html=True)
    ecio = st.number_input(
        "",
        min_value=-30.0,
        max_value=0.0,
        step=0.1,
        format="%.1f",
        help="Rango: -30 (Malo) a 0 (Excelente)",
        label_visibility="collapsed" 
    )

    st.markdown("<h6>⚡ Transmision Power [-50 dBm (Excelente) a 23 dBm (Malo)]</h6>", unsafe_allow_html=True)
    txpower = st.number_input(
        "",
        min_value=-50.0,
        max_value=23.0,
        step=0.1,
        format="%.1f",
        help="Rango: -50 dBm (Excelente) a 23 dBm (Malo)",
        label_visibility="collapsed" 
    )

    st.markdown("<h6>❌ BLER [0 (Excelente) a 1 (100% de Falla)]</h6>", unsafe_allow_html=True)
    bler = st.number_input(
        "",
        min_value=0.0,
        max_value=1.0,
        step=0.01,
        format="%.2f",
        help="Rango: 0 (Excelente) a 1 (100% de Falla)",
        label_visibility="collapsed" 
    )

    st.markdown("<h6>📊 RSSI [-130 dBm (Excelente) a -50 dBm (Malo)]</h6>", unsafe_allow_html=True)
    rssi = st.number_input(
        "",
        min_value=-130.0,
        max_value=-50.0,
        step=0.1,
        format="%.1f",
        help="Rango: -130 dBm (Excelente) a -50 dBm (Malo)",
        label_visibility="collapsed" 
    )


    speechcode_options = {
        "EFR": 4.7,
        "AMR Full Rate": 4.5,
        "AMR Half Rate": 4.41,
        "AMR WB": 4.36,
        "Full Rate": 4.16,
        "Half Rate": 3.95
    }
    st.markdown("<h6>🎙️ Speech Code</h6>", unsafe_allow_html=True)
    speechcode_label = st.selectbox(
        "",
        options=list(speechcode_options.keys()),
        help="Selecciona el tipo de codec de voz",
        label_visibility="collapsed" 
    )

    # Botón de enviar
    submit_button = st.form_submit_button(label="Predecir MOS")


# Procesar la predicción
if submit_button:
    speechcode = speechcode_options[speechcode_label]

    # Aqui llevo las variables del Formulario a un Dataframe que inyeco en el modelo
    dato_crudo = [ecio, rsrp, txpower, bler, rssi, speechcode]
    df_test = pd.DataFrame([dato_crudo], columns=[
        'wcdma_aset_ecio_avg',
        'wcdma_aset_rscp_avg',
        'wcdma_txagc',
        'wcdma_bler_average_percent_all_channels',
        'wcdma_rssi',
        'gsm_speechcodecrx'
    ])

    try:
        y_pred = modelopredictor.predict(df_test)
        pred_class = float(y_pred[0])
        st.markdown(f"<h3>Predicción del MOS: {pred_class:.2f}</h3>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error en la predicción: {str(e)}")