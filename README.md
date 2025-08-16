# PROYECTO STREAMLIT

La version funcional de Este proyecto se esta ejecutando en el siguiente URL
[https://26bwebappflask-production.up.railway.app/](https://overflowing-courage-production.up.railway.app/)

La idea detras de este proyecto es crear un calculo del MOS WCDMA en un determinado punto.   El MOS (Mean Opinion Score) es una medida de percepción de la calidad de la Red que experimenta un usuario.   El MOS el un valor que tiene una escalad de 1 a 5 donde 1 es muy malo y 5 muy bueno.

## NOTA: el modelo fue creado cuando se hizo la tarea de flask.  En esta tare lo que cambia es el desarrollo de la GUI con streamlink y la puesta en servicio.

## ESTRUCTURA

The proyecto esta organizado de la siguiente manera:

- **`app_streamlit.py`** → Es la aplicación que ejecuta el servicio del server de streamlit.
- **`src/Creacion_Modelo.ipynb`** → Notebook que contiene la creación del modelo del MOS.  Este modelo se creo en la tarea de FLask.



## Ejecutar la Aplicacion

Para ejecutar la aplicación se debe correr el servicio de streamlit a trave del archivo app_streamlit.py que esta en el directorio src:

Ejecutando:
streamlit run app_streamlit.py
