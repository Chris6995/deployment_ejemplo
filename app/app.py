import streamlit as st
import cv2
import joblib
from streamlit_drawable_canvas import st_canvas

# Cargar el modelo y el escalador
rf_clf = joblib.load("../model/rf_mnist_model.pkl")
scaler = joblib.load("../data/scaler.pkl")

st.title("Clasificador de Números Escritos a Mano")

# Crear una interfaz para dibujar
canvas_result = st_canvas(
    fill_color="white",
    stroke_width=10,
    stroke_color="black",
    background_color="white",
    width=280,
    height=280,
    drawing_mode="freedraw",
    key="canvas",
)

# Cuando se presiona el botón de clasificar
if st.button("Clasificar"):
    if canvas_result.image_data is not None:
        # Convertir la imagen a escala de grises y redimensionar a 28x28
        img = cv2.cvtColor(canvas_result.image_data, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (28, 28))
        img = img.reshape(1, -1)
        
        # Llamar al preprocessing
        img_scaled = scaler.transform(img.astype(float))
        
        # Predecir con el modelo entrando
        prediction = rf_clf.predict(img_scaled)
        
        st.write(f"El modelo predice que es un: {prediction[0]}")

st.sidebar.title("Acerca de")
st.sidebar.info(
    """
    Esta aplicación utiliza un modelo RF entrenado con los datos de MNIST para clasificar números manuscritos.
    Dibuje un número en el canvas y presione "Clasificar" para ver la predicción.
    """
)