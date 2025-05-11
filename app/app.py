import streamlit as st
import pickle
import numpy as np

# Load model
with open('../model/ev_model.pkl', 'rb') as f:
    model = pickle.load(f)

st.title("🔋 EV Range Estimator")
st.write("Enter the following details to predict remaining range:")

# Input fields
battery_voltage = st.slider('Battery Voltage (V)', 300, 400, 360)
current = st.slider('Current (A)', 10, 100, 45)
temperature = st.slider('Battery Temperature (°C)', 0, 60, 30)
soc = st.slider('State of Charge (%)', 0, 100, 75)
speed = st.slider('Vehicle Speed (km/h)', 0, 120, 50)
load = st.slider('Vehicle Load (kg)', 0, 500, 150)

if st.button("🚀 Predict Range"):
    input_data = np.array([[battery_voltage, current, temperature, soc, speed, load]])
    prediction = model.predict(input_data)
    st.success(f"🔋 Estimated Range: {prediction[0]:.2f} km")
