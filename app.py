import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Prediksi Obesitas", layout="centered")
st.markdown("""
    <style>
    .main { background-color: #f5f7fa; }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5em 1em;
    }
    .stTextInput, .stNumberInput, .stSelectbox {
        border-radius: 8px;
        background-color: #ffffff;
        padding: 0.25em;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Aplikasi Prediksi Tingkat Obesitas")
st.markdown("""
Gunakan aplikasi ini untuk memprediksi tingkat obesitas berdasarkan data pribadi dan kebiasaan hidup.
Silakan unggah file CSV atau isi data secara manual.
""")

# Load model
@st.cache_data
def load_model():
    return joblib.load("model.pkl")

model = load_model()

# Upload file CSV
uploaded = st.file_uploader("📂 Upload file CSV data pasien", type=["csv"])
if uploaded:
    df = pd.read_csv(uploaded)
    st.markdown("**Data Preview:**")
    st.dataframe(df.head(), use_container_width=True)

st.markdown("---")
st.subheader("📝 Input Data Manual")

# Daftar fitur yang diharapkan model
EXPECTED_FEATURES = [
    'Age', 'Gender', 'Height', 'Weight', 'CALC', 'FAVC', 'FCVC', 'NCP', 'SCC',
    'SMOKE', 'CH2O', 'family_history_with_overweight', 'FAF', 'TUE', 'CAEC', 'MTRANS'
]

# Input manual
inputs = {}
cols = st.columns(2)
inputs["Age"] = cols[0].number_input("Usia", min_value=0, step=1)
inputs["Gender"] = cols[1].selectbox("Jenis Kelamin", ["Male", "Female"])

cols = st.columns(2)
inputs["Height"] = cols[0].number_input("Tinggi Badan (m)", min_value=0.0, step=0.01)
inputs["Weight"] = cols[1].number_input("Berat Badan (kg)", min_value=0.0, step=0.01)

cols = st.columns(2)
inputs["CALC"] = cols[0].selectbox("Konsumsi Alkohol", ["Sometimes", "no"])
inputs["FAVC"] = cols[1].selectbox("Konsumsi Makanan Tinggi Kalori", ["yes", "no"])

cols = st.columns(2)
inputs["FCVC"] = cols[0].number_input("Frekuensi Konsumsi Sayur", min_value=0, step=1)
inputs["NCP"] = cols[1].number_input("Jumlah Makan Utama per Hari", min_value=0.0, step=0.1)

cols = st.columns(2)
inputs["SCC"] = cols[0].selectbox("Makan di Luar Waktu Makan", ["Sometimes", "no"])
inputs["SMOKE"] = cols[1].selectbox("Merokok", ["yes", "no"])

cols = st.columns(2)
inputs["CH2O"] = cols[0].number_input("Konsumsi Air per Hari (liter)", min_value=0.0, step=0.1)
inputs["family_history_with_overweight"] = cols[1].selectbox("Riwayat Keluarga Obesitas", ["yes", "no"])

cols = st.columns(2)
inputs["FAF"] = cols[0].number_input("Aktivitas Fisik (jam/minggu)", min_value=0.0, step=0.1)
inputs["TUE"] = cols[1].number_input("Waktu Hiburan Teknologi (jam)", min_value=0, step=1)

cols = st.columns(2)
inputs["CAEC"] = cols[0].selectbox("Kebiasaan Konsumsi Alkohol", ["Sometimes", "no"])
inputs["MTRANS"] = cols[1].selectbox("Transportasi Utama", ["Automobile", "Motorbike", "Public_Transportation", "Walking"])

# Buat DataFrame dari input manual
X = pd.DataFrame([inputs])

# Konversi kolom kategorikal menjadi angka (jika diperlukan oleh model)
categorical_cols = X.select_dtypes(include=['object']).columns
for col in categorical_cols:
    X[col] = X[col].astype('category').cat.codes

# Ringkasan input
st.markdown("---")
st.markdown("### 🔍 Ringkasan Input")
st.json(inputs)

# Prediksi obesitas
if st.button("Prediksi Obesitas"):
    yhat = model.predict(X)[0]  # hasil prediksi berupa string label kelas

    # Deskripsi hasil prediksi dalam Bahasa Indonesia
    prediction_description = {
        'Insufficient_Weight': "Berat badan anda kurang",
        'Normal_Weight': "Berat badan anda normal",
        'Overweight_Level_I': "Kelebihan berat badan level I",
        'Overweight_Level_II': "Kelebihan berat badan level II",
        'Obesity_Type_I': "Obesitas Tipe I",
        'Obesity_Type_II': "Obesitas Tipe II",
        'Obesity_Type_III': "Obesitas Tipe III"
    }
