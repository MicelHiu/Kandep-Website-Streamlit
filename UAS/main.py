import streamlit as st
import pandas as pd 

#Title
st.title("TENANT KANDEP")
st.write("Rekomendasi dari TOP 3 Program Studi terbanyak")
st.markdown("---")

menu = st.sidebar.selectbox(
    "Pilih Halaman",
    ["Beranda","About us"]
)

st.subheader("Informatika")

if menu == "Beranda":
    st
