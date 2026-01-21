import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# -----------------------------
# SAMPLE TRAINING DATA
# -----------------------------
data = {
    "temperature": [30, 34, 28, 36, 32, 38],
    "rainfall": [5, 0, 12, 0, 6, 0],
    "humidity": [65, 55, 75, 50, 60, 48],
    "irrigation": [12, 18, 10, 20, 14, 22],
    "crop_need": [12, 14, 10, 15, 13, 16],
    "yield_loss": [2, 10, 1, 18, 5, 22]
}

df = pd.DataFrame(data)

X = df[["temperature", "rainfall", "humidity", "irrigation", "crop_need"]]
y = df["yield_loss"]

model = RandomForestRegressor(n_estimators=50, random_state=42)
model.fit(X, y)

# -----------------------------
# LOGIC FUNCTIONS
# -----------------------------
def crop_stress(balance):
    if balance >= 0:
        return "No Stress"
    elif -3 <= balance < 0:
        return "Mild Stress"
    elif -6 <= balance < -3:
        return "Moderate Stress"
    else:
        return "Severe Stress"

def water_wastage(balance):
    if balance <= 0:
        return "No Wastage"
    elif balance <= 3:
        return "Low Wastage"
    elif balance <= 6:
        return "Medium Wastage"
    else:
        return "High Wastage"

def irrigation_type(irrigation, crop_need, rainfall):
    if irrigation == crop_need and rainfall == 0:
        return "Uniform Irrigation"
    return "Non-Uniform Irrigation"

def recommendations(stress, wastage, irrigation_type, loss):
    rec = []

    if stress == "Mild Stress":
        rec.append("Increase irrigation slightly and monitor crop daily.")
    elif stress == "Moderate Stress":
        rec.append("Apply irrigation in split cycles and avoid midday watering.")
    elif stress == "Severe Stress":
        rec.append("Immediate irrigation required to prevent crop damage.")

    if wastage in ["Medium Wastage", "High Wastage"]:
        rec.append("Reduce irrigation quantity by 20–30%.")
        rec.append("Avoid irrigation when rainfall is expected.")

    if irrigation_type == "Non-Uniform Irrigation":
        rec.append("Adjust irrigation based on crop stage and soil condition.")

    if loss > 10:
        rec.append("High income loss risk detected. Correct irrigation immediately.")

    if not rec:
        rec.append("Current irrigation practice is optimal.")

    return rec

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="AI Irrigation Advisor", layout="centered")

st.title("🌾 AI-Based Irrigation Risk & Income Loss Prediction")

temperature = st.number_input("Temperature (°C)", 10.0, 50.0, 30.0)
rainfall = st.number_input("Rainfall (mm)", 0.0, 50.0, 0.0)
humidity = st.number_input("Humidity (%)", 10.0, 100.0, 60.0)
irrigation = st.number_input("Irrigation Amount (mm)", 0.0, 50.0, 15.0)
crop_need = st.number_input("Crop Water Requirement (mm)", 0.0, 50.0, 12.0)

if st.button("Predict"):
    input_data = pd.DataFrame([{
        "temperature": temperature,
        "rainfall": rainfall,
        "humidity": humidity,
        "irrigation": irrigation,
        "crop_need": crop_need
    }])

    loss = model.predict(input_data)[0]
    balance = irrigation + rainfall - crop_need

    st.subheader("📊 Prediction Results")
    st.write("🌱 Crop Stress Level:", crop_stress(balance))
    st.write("💧 Water Wastage Level:", water_wastage(balance))
    st.write("🚿 Irrigation Type:", irrigation_type(irrigation, crop_need, rainfall))
    st.write("💰 Estimated Income Loss: ₹", round(loss * 200, 2))

    st.subheader("📌 Irrigation Recommendations")
    for r in recommendations(crop_stress(balance), water_wastage(balance),
                              irrigation_type(irrigation, crop_need, rainfall), loss):
        st.write("•", r)
