import streamlit as st
import pandas as pd
import numpy as np
import joblib

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")


# Deskripsi singkat
st.markdown(
    """
    Aplikasi ini memprediksi tingkat obesitas berdasarkan data yang dimasukkan.
    """
)

# Load model
@st.cache_data
def load_model():
    return joblib.load("model.pkl")

model = load_model()

import streamlit as st

# Header utama
st.title("Prediksi Tingkat Obesitas")

# Deskripsi singkat
st.markdown(
    """
    Aplikasi ini memprediksi tingkat obesitas berdasarkan data yang dimasukkan.
    """
)

# Input data dalam kolom dua bagian
col1, col2 = st.columns(2)

with col1:
    # Age
    age = st.number_input("Age", min_value=0, step=1)
    # Height
    height = st.number_input("Height (in meters)", min_value=0.0, step=0.01)
    # FAVC
    favc = st.selectbox("FAVC (Yes/No)", ["yes", "no"])

with col2:
    # Gender
    gender = st.selectbox("Gender (Male/Female)", ["Male", "Female"])
    # Weight
    weight = st.number_input("Weight (in kg)", min_value=0.0, step=0.01)
    # CALC
    calc = st.selectbox("CALC (Sometimes/No)", ["Sometimes", "no"])

# Tampilkan input lainnya di bawah
st.subheader("Lifestyle and Habits")
# FCVC
fcvc = st.number_input("FCVC (Frequency of consuming vegetables)", min_value=0, step=1)
# NCP
ncp = st.number_input("NCP (Number of main meals)", min_value=0.0, step=0.1)
# SCC
scc = st.selectbox("SCC (Consumption of food between meals)", ["Sometimes", "no"])
# SMOKE
smoke = st.selectbox("SMOKE (Smoking habit)", ["yes", "no"])
# CH2O
ch2o = st.number_input("CH2O (Daily consumption of water)", min_value=0.0, step=0.1)
# family_history_with_overweight
family_history = st.selectbox("Family History with Overweight (Yes/No)", ["yes", "no"])
# FAF
faf = st.number_input("FAF (Physical Activity Frequency)", min_value=0.0, step=0.1)
# TUE
tue = st.number_input("TUE (Time Using Technology for Entertainment)", min_value=0, step=1)
# CAEC
caec = st.selectbox("CAEC (Consumption of alcohol)", ["Sometimes", "no"])
# MTRANS
mtrans = st.selectbox("MTRANS (Mode of Transportation)", ["Automobile", "Motorbike", "Public_Transportation", "Walking"])


# Buat DataFrame dari input
   X = pd.DataFrame([inputs])

   # Encode fitur kategorikal
   categorical_cols = X.select_dtypes(include=['object']).columns
   for col in categorical_cols:
       X[col] = X[col].astype('category').cat.codes

   st.subheader("Input untuk prediksi:")
   st.json(inputs)

   if st.button("Prediksi"):
       yhat = model.predict(X)[0]
       st.success(f"Prediksi berhasil! Prediksi obesitas: **{yhat}**")
       if hasattr(model, "predict_proba"):
           probs = model.predict_proba(X)[0]
           st.write("Probabilitas per kelas:")
           st.json(dict(zip(model.classes_, [float(p) for p in probs])))
           


