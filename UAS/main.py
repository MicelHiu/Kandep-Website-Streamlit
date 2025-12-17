import streamlit as st
import pandas as pd
from model import load_model, predict_tenant 

def convert_budget(budget):
    if budget < 10000:
        return "< 10.000"
    elif 10000 <= budget <= 20000:
        return "10.000 - 20.000"
    elif 21000 <= budget <= 30000:
        return "21.000 - 30.000"
    else:
        return "> 30.000"

def load_css():
    st.markdown("""
    <style>
    .stApp {
        background-color: #FBE6A1;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #2E5AA7;        
    }
                
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] label {
        color: white;
    }
    
    h1 {
        color: #2E5AA7;
        font-weight: 800;
    }
    
    input, textarea, select {
        border-radius: 10px !important;
        border: 1px solid #86C5FF !important;
    }
                
    
    div.stButton > button {
        background-color: #FFA62B;
        color: #2E5AA7;
        border-radius: 12px;
        padding: 0.6rem 1.4rem;
        font-weight: bold;
        border: none;
    }
                
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.12);
    }
    
    hr {
        border: none;
        height: 2px;
        background-color: #2E5AA7;
    }
    </style>
    
""", unsafe_allow_html=True)
@st.cache_resource
def load_ml():
    return load_model()
model, encoders = load_ml()

#Halaman
st.set_page_config(page_title="KANDEP", layout="wide")

load_css()

#State
if "page" not in st.session_state:
    st.session_state.page = "Beranda"

#Sidebar
pages = ["Beranda","Hasil Rekomendasi","About Us"]

st.sidebar.title("Menu")
menu = st.sidebar.radio(
    "Pilih Halaman",
    pages,
    index=pages.index(st.session_state.page)
)

#update halama jika berubah
if menu != st.session_state.page:
    st.session_state.page = menu

#Halaman Beranda
if st.session_state.page == "Beranda":
    st.title("KANDEP")
    st.write("Semua Rasa Lapar dan Hausmu bisa diatasi dari Web ini")
    st.markdown("---")

    #input data
    prodi = st.selectbox(
        "Program Studi Anda?",
        encoders["Program Studi"].classes_
    )

    #input harga
    budget = st.slider(
        "Budget Pengeluaran (Rp)",
        min_value=5000,
        max_value=50000,
        step=5000
    )

    #Pilih Jenis Makanan
    jenis_makanan = st.selectbox(
        "Mau beli apa?",
        encoders["Menu apa yang paling sering Anda pesan?"].classes_
    )

    st.markdown("---")
    if st.button("OK"):
        st.session_state.prodi = prodi
        st.session_state.budget = convert_budget(budget)
        st.session_state.jenis_makanan = jenis_makanan
        
        #PINDAH HALAMAN
        st.session_state.page = "Hasil Rekomendasi"
        st.rerun()

#Hasil Rekomendasi
elif st.session_state.page == "Hasil Rekomendasi":
    st.title("Hasil Rekomendasi Tenant")
    st.markdown("---")

    prodi = st.session_state.get("prodi")
    budget = st.session_state.get("budget")
    jenis_makanan = st.session_state.get("jenis_makanan")

    st.write(f"**ProgramStudi:** {prodi}")
    st.write(f"**Budget:**  {budget}")
    st.write(f"**Kategori:** {jenis_makanan}")

    st.markdown("---")

    try:
        top3 = predict_tenant(
            model,
            encoders,
            st.session_state.prodi,
            st.session_state.budget,
            st.session_state.jenis_makanan,
        )
        st.subheader("3 Tenant Teratas untuk Anda:")
        for i, row in top3.iterrows():
            st.markdown(
                 f"### 🏪 {row['Tenant']}\n"
                f"Relevansi: **{row['Probabilitas']*100:.2f}%**"
            )
    except Exception as e:
        st.error("Data input tidak dikenali oleh mesin.")
        st.caption(str(e))
    
    st.markdown("---")
    if st.button("Coba lagi"):
        st.session_state.page = "Beranda"
        st.rerun()

#Halaman US
elif st.session_state.page == "About Us":
    st.title("ABOUT US")
    st.markdown("""
        Kelompok 3 
        Bene - 202310 
        Catur - 202310 
        Michelle - 202310 
        Najla - 2023105534
        """, unsafe_allow_html=True)
