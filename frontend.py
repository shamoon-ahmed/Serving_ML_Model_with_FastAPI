import streamlit as st
import requests

URL = 'http://127.0.0.1:8000/predict'

st.title("Acne Risk Predictor")

st.markdown("Enter a few details below and know if you have risk of developing acne:")

# Input fields
age = st.number_input("Age", min_value=1, max_value=119, value=30)
gender = st.selectbox("Gender", options=['male', 'female'])
weight_kg = st.number_input("Weight (kg)", min_value=1.0, value=65.0)
diet = st.selectbox("Diet", options=['healthy', 'unhealthy'])
sleep_hours = st.number_input("How many hours do you sleep?", min_value=1.0, value=10.0)
water_intake_liters = st.number_input("How many liters of water do you drink in a day?", min_value=0.1, value=10.0)
smoking_or_vaping = st.selectbox("Do you smoke or vape?", options=['yes', 'no'])

if st.button("Predict Acne Risk"):
    input_data = {
        "age": age,
        "gender": gender,
        "weight_kg": weight_kg,
        "diet": diet,
        "sleep_hours": sleep_hours,
        "water_intake_liters": water_intake_liters,
        "smoking_or_vaping": smoking_or_vaping
    }

    try:
        response = requests.post(URL, json=input_data)
        result = response.json()

        if response.status_code == 200 or response.status_code == 201:
            st.success(f"Acne Risk Precition: {result['message']}")

        else:
            st.error(f"API Error: {response.status_code}")

    except requests.exceptions.ConnectionError:
        st.error('Server Error!')


# input_data = {
#         "age": 22,
#         "gender": 'male',
#         "weight_kg": 55,
#         "diet": 'unhealthy',
#         "sleep_hours": 2.0,
#         "water_intake_liters": 0.1,
#         "smoking_or_vaping": 'yes'
#     }

# response = requests.post(URL, json=input_data)
# result = response.json()
# print(result)