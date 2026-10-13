import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from model import load_model, predict_tenant 

#Halaman
st.set_page_config(page_title="KANDEP", layout="wide")

def convert_budget(budget):
    if budget < 10000:
        return "< Rp10.000"
    elif 10000 <= budget <= 20000:
        return "10.000 - 20.000"
    elif 21000 <= budget <= 30000:
        return "21.000 - 30.000"
    else:
        return "> 30.000"

PALETTES = {
    "light": {
        "bg": "#FFFFFF", "text": "#1B2B4B", "accent": "#2E5AA7", "card": "#F4F7FC",
        "btn_text": "#1B2B4B", "sidebar_bg": "#2E5AA7", "sidebar_text": "#FFFFFF",
    },
    "dark": {
        "bg": "#000000", "text": "#F5F5F5", "accent": "#86C5FF", "card": "#1A1A1A",
        "btn_text": "#000000", "sidebar_bg": "#111111", "sidebar_text": "#FFFFFF",
    },
}

def current_theme():
    # follows the active Streamlit theme (Settings > Theme), not the OS
    try:
        return "dark" if st.context.theme.type == "dark" else "light"
    except Exception:
        return "light"

THEME = current_theme()
COLORS = PALETTES[THEME]

def load_css():
    c = COLORS
    st.markdown(
        f"""<style>:root {{
            --bg: {c['bg']}; --text: {c['text']}; --accent: {c['accent']};
            --card: {c['card']}; --btn-text: {c['btn_text']};
            --sidebar-bg: {c['sidebar_bg']}; --sidebar-text: {c['sidebar_text']};
        }}</style>""",
        unsafe_allow_html=True,
    )
    st.markdown("""
    <style>
    .stApp {
        background-color: var(--bg);
        font-family: 'Segoe UI', sans-serif;
    }

    /* Main content text follows the theme */
    section.main p,
    section.main label,
    section.main span,
    [data-testid="stMain"] p,
    [data-testid="stMain"] label,
    [data-testid="stMain"] span,
    [data-testid="stMain"] li {
        color: var(--text) !important;
    }

    section.main h1,
    section.main h2,
    section.main h3,
    section.main h4,
    section.main h5,
    section.main h6,
    [data-testid="stMain"] h1,
    [data-testid="stMain"] h2,
    [data-testid="stMain"] h3,
    [data-testid="stMain"] h4,
    [data-testid="stMain"] h5,
    [data-testid="stMain"] h6 {
        color: var(--accent) !important;
        font-weight: 800;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] label {
        color: var(--sidebar-text);
    }

    input, textarea, select {
        border-radius: 10px !important;
        border: 1px solid #86C5FF !important;
    }

    div.stButton > button {
        background-color: #FFA62B;
        color: var(--btn-text);
        border-radius: 12px;
        padding: 0.6rem 1.4rem;
        font-weight: bold;
        border: none;
    }

    .card {
        background-color: var(--card);
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.12);
    }

    hr {
        border: none;
        height: 2px;
        background-color: var(--accent);
    }
    </style>

""", unsafe_allow_html=True)
    
def load_ml():
    return load_model()
model, encoders = load_ml()

load_css()

#State
MENU = ["Beranda", "Tentang Kami"]

if "view" not in st.session_state:
    st.session_state.view = "form"  # "form" | "hasil" (sub-halaman Beranda)
if "menu" not in st.session_state:
    st.session_state.menu = "Beranda"

#Sidebar
with st.sidebar:
    selected = option_menu(
        menu_title="Menu",
        options=MENU,
        icons=["house", "info-circle"],
        menu_icon="list",
        default_index=MENU.index(st.session_state.menu),
        styles={
            "container": {"padding": "10px", "background-color": COLORS["sidebar_bg"]},
            "icon": {"font-size": "18px", "color": "white"},
            "nav-link": {
                "font-size": "16px",
                "color": "white",
                "margin": "6px",
                "--hover-color": "#3A6EDC",
            },
            "nav-link-selected": {
                "background-color": "#FFA62B",
                "color": "#2E5AA7",
                "font-weight": "bold",
            },
        }
    )

# pindah menu -> Beranda selalu mulai dari form
if selected != st.session_state.menu:
    st.session_state.menu = selected
    st.session_state.view = "form"


#Halaman Beranda (form input)
if st.session_state.menu == "Beranda" and st.session_state.view == "form":
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

        #buka sub-halaman hasil di dalam Beranda
        st.session_state.view = "hasil"
        st.rerun()

#Beranda > Hasil Rekomendasi
elif st.session_state.menu == "Beranda" and st.session_state.view == "hasil":
    st.title("Hasil Rekomendasi Tenant")
    st.markdown("---")

    prodi = st.session_state.get("prodi")
    budget = st.session_state.get("budget")
    jenis_makanan = st.session_state.get("jenis_makanan")

    st.write(f"**Program Studi:** {prodi}")
    st.write(f"**Budget:**  {budget}")
    st.write(f"**Kategori:** {jenis_makanan}")

    st.markdown("---")

    try:
        top3 = predict_tenant(
            model,
            encoders,
            prodi,
            budget,
            jenis_makanan
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
    if st.button("← Kembali ke Beranda"):
        st.session_state.view = "form"
        st.rerun()

#Halaman Tentang Kami
elif st.session_state.menu == "Tentang Kami":
    st.title("TENTANG KAMI")
    st.markdown("""
        Halo user! Program ini merupakan website rekomendasi tenant kantin depan Universitas Kalbis yang dapat membantu kalian dalam memilih tenant sesuai dengan preferensi masing-masing. Perlu diingat bahwa website ini masih dalam tahap pengembangan, jadi mohon maaf apabila terdapat kekurangan atau error pada saat penggunaan dan nantikan update selanjutnya ya!\n\n
        
        Website ini dibuat oleh:\n
        1. Michelle Hiu (2023105488)\n
        2. Najla Melinda Kiasati (2023105534)\n
        3. Benediktus Nikolistyawan (2023105489)\n
        4. Catur Bakti Prajna (2023105533)\n
        """, unsafe_allow_html=True)
