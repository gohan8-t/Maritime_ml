import streamlit as st
import requests
import pandas as pd
from fpdf import FPDF

st.set_page_config(page_title="Emissions Dashboard", layout="centered")
st.title("🚢 Emissions Dashboard")

fuel_type = st.selectbox("Fuel Type", ["HFO", "VLSFO", "MDO", "LNG"])
speed = st.number_input("Speed (knots)", min_value=1.0, value=14.0)
engine_load = st.number_input("Engine Load (%)", min_value=1.0, max_value=100.0, value=85.0)
draft = st.number_input("Draft (meters)", min_value=5.0, value=11.0)
sea_state = st.number_input("Sea State Index (1-7)", min_value=1, max_value=7, value=4)
ambient_temp = st.number_input("Ambient Temperature (°C)", value=20.0)
cargo_weight = st.number_input("Cargo Weight (tons)", value=100000.0)
hull_fouling = st.slider("Hull Fouling Index", 0.0, 1.0, 0.3)
distance = st.number_input("Distance Sailed (NM)", value=500.0)
tonnage = st.number_input("Gross Tonnage (GT)", value=50000.0)

if st.button("Run Emissions Check"):
    rule_payload = {
        "fuel_type": fuel_type,
        "fuel_used_liters": engine_load * 10,
        "distance_nm": distance,
        "gross_tonnage": tonnage
    }
    ml_payload = {
        "fuel_type": fuel_type,
        "speed_knots": speed,
        "engine_load_pct": engine_load,
        "draft_meters": draft,
        "sea_state_index": sea_state,
        "ambient_temp": ambient_temp,
        "cargo_weight": cargo_weight,
        "hull_fouling_index": hull_fouling
    }

    try:
        rule = requests.post("http://api:5000/check_emissions", json=rule_payload).json()
        st.success(rule["compliance_status"])
        st.metric("Rule-Based CO₂", rule["total_emissions_kg"])
    except:
        st.error("Rule API failed")

    try:
        ml = requests.post("http://ml-api:5000/predict_co2", json=ml_payload).json()
        st.metric("ML-Predicted CO₂", ml["predicted_co2_kgph"])
    except:
        st.error("ML API failed")