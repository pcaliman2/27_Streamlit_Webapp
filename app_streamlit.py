import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Predictor de MOS WCDMAxc", page_icon="📡")

modelopredictor = joblib.load("modelo_randon_forest_200_10_5_2.pkl")



st.markdown(
    """
    <style>
    .stApp {
        background-image: url("/src/static/fondo.jpg");
        background-size: cover;        /* cubre toda la ventana */
        background-position: center;   /* centra la imagen */
        background-repeat: no-repeat;  /* evita que se repita */
    }
    </style>
    """,
    unsafe_allow_html=True
)




# Título
st.title("Predictor de MOS WCDMA")

# Formulario
with st.form(key="mos_predictor_form"):
    # RSCP
    rsrp = st.number_input(
        "📶 RSCP (Received Signal Code Power) [-130 dBm (Malo) a -50 dBm]",
        min_value=-130.0,
        max_value=-50.0,
        step=0.1,
        format="%.1f",
        help="Rango: -130 dBm (Malo) a -50 dBm (Excelente)"
    )

    # ECIO
    ecio = st.number_input(
        "📡 ECIO (Energy per Chip to Interference) [-30 (Malo) a 0 (Excelente)]",
        min_value=-30.0,
        max_value=0.0,
        step=0.1,
        format="%.1f",
        help="Rango: -30 (Malo) a 0 (Excelente)"
    )

    # Transmision Power
    txpower = st.number_input(
        "⚡ Transmision Power [-50 dBm (Excelente) a 23 dBm (Malo)]",
        min_value=-50.0,
        max_value=23.0,
        step=0.1,
        format="%.1f",
        help="Rango: -50 dBm (Excelente) a 23 dBm (Malo)"
    )

    # BLER
    bler = st.number_input(
        "❌ BLER [0 (Excelente) a 1 (100% de Falla)]",
        min_value=0.0,
        max_value=1.0,
        step=0.01,
        format="%.2f",
        help="Rango: 0 (Excelente) a 1 (100% de Falla)"
    )

    # RSSI
    rssi = st.number_input(
        "📊 RSSI [-130 dBm (Excelente) a -50 dBm (Malo)]",
        min_value=-130.0,
        max_value=-50.0,
        step=0.1,
        format="%.1f",
        help="Rango: -130 dBm (Excelente) a -50 dBm (Malo)"
    )

    # Speech Code
    speechcode_options = {
        "EFR": 4.53,
        "AMR Full Rate": 4.5,
        "AMR Half Rate": 4.41,
        "AMR WB": 4.36,
        "Full Rate": 4.16,
        "Half Rate": 3.95
    }
    speechcode_label = st.selectbox(
        "🎙️ Speech Code",
        options=list(speechcode_options.keys()),
        help="Selecciona el tipo de codec de voz"
    )

    # Botón de enviar
    submit_button = st.form_submit_button(label="Predecir MOS")

# Procesar la predicción
if submit_button:
    # Obtener el valor numérico del speech code
    speechcode = speechcode_options[speechcode_label]

    # Crear el DataFrame con los nombres de columnas originales
    dato_crudo = [ecio, rsrp, txpower, bler, rssi, speechcode]
    df_test = pd.DataFrame([dato_crudo], columns=[
        'wcdma_aset_ecio_avg',
        'wcdma_aset_rscp_avg',
        'wcdma_txagc',
        'wcdma_bler_average_percent_all_channels',
        'wcdma_rssi',
        'gsm_speechcodecrx'
    ])

    # Hacer la predicción
    try:
        y_pred = modelopredictor.predict(df_test)
        pred_class = float(y_pred[0])
        st.markdown(f"<h3>Predicción del MOS: {pred_class:.2f}</h3>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error en la predicción: {str(e)}")