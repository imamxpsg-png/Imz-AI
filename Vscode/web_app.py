import os
import streamlit as st
from groq import Groq

# Inisialisasi Groq Client
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 1. Konfigurasi Halaman Utama
st.set_page_config(page_title="AI Chat UI Premium", layout="centered")

# 2. Gaya CSS Kustom Dioptimalkan untuk Layar HP (Mobile Optimized)
st.markdown("""
    <style>
    /* Mengurangi padding default Streamlit agar area chat di HP lebih luas */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* 1. ANIMASI JUDUL ATAS (Ukuran disesuaikan untuk HP) */
    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .animated-title {
        font-size: 28px; /* Diperkecil dari 34px agar pas di layar HP */
        font-weight: 800;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 10px;
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientMove 8s ease infinite;
    }
    
    /* 2. GAYA TEKS PEMBUKA (Proporsional untuk HP) */
    .welcome-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 15vh; 
        text-align: center;
        margin-bottom: 10px;
        padding: 0 10px;
    }
    .welcome-text {
        font-size: 16px; /* Diperkecil ke 16px agar tidak patah berantakan di HP */
        font-weight: 500;
        color: #4a5568;
        line-height: 1.5;
    }
    
    /* 3. BINGKAI INPUT BAWAH YANG COMPACT UNTUK HP */
    [data-testid="stVerticalBlockBorderWrapper"] .custom-input-box {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 24px; /* Sedikit dikurangi lengkungannya agar rapi */
        padding: 6px 10px;  /* Padding dipersempit agar hemat ruang */
        box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
    }
    
    /* Menghilangkan border input bawaan asli */
    div[data-testid="stTextInput"] input {
        border: none !important;
        box-shadow: none !important;
        background-color: transparent !important;
        padding-left: 2px !important;
        font-size: 15px !important; /* Ukuran teks input standar HP */
        height: 38px !important;
    }
    
    /* Tombol Popover Plus Lingkaran Mini */
    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        background-color: #f1f3f4 !important;
        color: #333333 !important;
        border: none !important;
        height: 36px !important; /* Diperkecil dari 42px agar pas di jempol */
        width: 36px !important;
        min-width: 36px !important;
        max-width: 36px !important;
        padding: 0 !important;
        box-shadow: none !important;
    }

    /* Tombol Kirim 🚀 Mini */
    div.stButton > button[key="send_btn"] {
        background: linear-gradient(135deg, #1a73e8 0%, #1557b0 100%) !important;
        color: white !important;
        border-radius: 50% !important;
        border: none !important;
        height: 36px !important; /* Diperkecil menyesuaikan tombol plus */
        width: 36px !important;
        min-width: 36px !important;
        max-width: 36px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0px 2px 5px rgba(26, 115, 232, 0.2) !important;
    }

    /* Bubble Chat Responsif HP */
    .bubble-user {
        background-color: #f0f4f9;
        padding: 10px 14px;
        border-radius: 16px 16px 0px 16px;
        margin-bottom: 10px;
        max-width: 90%; /* Diperlebar sedikit agar menampung teks lebih banyak di layar sempit */
        margin-left: auto;
        color: #202124;
        font-size: 15px;
    }
    .bubble-ai {
        background-color: #ffffff;
        padding: 10px 14px;
        border-radius: 16px 16px 16px 0px;
        margin-bottom: 10px;
        max-width: 90%;
        border: 1px solid #e3e3e3;
        color: #202124;
        font-size: 15px;
    }
    
    /* Tombol Hapus Chat di dalam Popover */
    div.stButton > button[key="clear_btn"] {
        background-color: #ff4b4b !important;
        color: white !important;
        border-radius: 10px;
        border: none;
        width: 100%;
        padding: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Baris Atas Hanya Berisi Tulisan Imz-AI
st.markdown('<h1 class="animated-title">Imz-AI</h1>', unsafe_allow_html=True)
st.divider()

# Kamus bahasa beserta instruksi sistem untuk AI
opsi_bahasa = {
    "Bahasa Indonesia 🇮🇩": "Anda adalah asisten AI ramah yang wajib menjawab dalam Bahasa Indonesia.",
    "English 🇺🇸": "You are a helpful AI assistant. You must respond strictly in English.",
    "Japanese 🇯🇵": "あなたは親切なAIアシスタントです。必ず日本語で答えてください。",
    "Korean 🇰🇷": "당신은 친절한 AI 어시스턴트입니다. 반드시 한국어로 답변해 주세요.",
    "Chinese 🇨🇳": "你是一个友好的AI助手。请务必用中文回答。"
}

# 4. Inisialisasi Memori Percakapan & State Bahasa
if "messages" not in st.session_state:
    st.session_state.messages = []
if "bahasa_sekarang" not in st.session_state:
    st.session_state.bahasa_sekarang = "Bahasa Indonesia 🇮🇩"

# Tampilan Kondisional: Selamat Datang atau Riwayat Percakapan
if not st.session_state.messages:
    st.markdown(
        '<div class="welcome-container"><p class="welcome-text">Selamat datang di Imz-AI, <br>apa ada yang bisa dibantu?</p></div>', 
        unsafe_allow_html=True
    )
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='bubble-user'><b>Anda:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
        elif msg["role"] == "assistant":
            st.markdown(f"<div class='bubble-ai'><b>AI:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

# 5. Fungsi Eksekusi Pengiriman Pesan
def kirim_pesan():
    user_text = st.session_state.get("input_box", "").strip()
    if user_text:
        context = ""
        if st.session_state.get("file_upload"):
            context += f"\n\n[File teks terlampir: {st.session_state.file_upload.name}]"
        if st.session_state.get("img_upload"):
            context += f"\n\n[*Mengunggah foto: {st.session_state.img_upload.name}*]"
            
        st.session_state.messages.append({"role": "user", "content": user_text + context})
        
        try:
            system_instruction = opsi_bahasa[st.session_state.bahasa_sekarang]
            history = [{"role": "system", "content": system_instruction}]
            history.extend([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages])
            
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=history
            )
            st.session_state.messages.append({"role": "assistant", "content": completion.choices.message.content})
        except Exception as e:
            st.session_state.messages.append({"role": "assistant", "content": f"Gagal memproses: {e}"})
        
        st.session_state["input_box"] = ""

def hapus_obrolan():
    st.session_state.messages = []
    if "img_upload" in st.session_state:
        del st.session_state["img_upload"]
    if "file_upload" in st.session_state:
        del st.session_state["file_upload"]

# 6. BINGKAI UTAMA: Rasio Lebar Kolom Dioptimalkan untuk HP ([1.5, 7.0, 1.5])
st.write("") 
with st.container(border=False):
    st.markdown('<div class="custom-input-box">', unsafe_allow_html=True)
    
    # Rasio kolom disesuaikan agar kotak ketik teks tetap luas di layar HP yang sempit
    col_popover, col_input, col_send = st.columns([1.5, 7.0, 1.5], vertical_alignment="center")
    
    with col_popover:
        with st.popover("＋"):
            st.caption("📂 **Lampiran & Alat**")
            st.file_uploader("🖼️ Upload gambar", type=["png", "jpg", "jpeg"], key="img_upload")
            st.file_uploader("📄 Upload file", type=["txt", "pdf"], key="file_upload")
            
            st.divider()
            st.caption("🎨 **Alat Tambahan**")
            if st.button("Buat gambar", use_container_width=True):
                st.toast("Fitur pembuatan gambar aktif!")
                
            st.divider()
            st.caption("🌐 **Pengaturan Bahasa**")
            st.session_state.bahasa_sekarang = st.selectbox(
                "Pilih Bahasa Respon AI:",
                options=list(opsi_bahasa.keys()),
                index=list(opsi_bahasa.keys()).index(st.session_state.bahasa_sekarang),
                label_visibility="collapsed"
            )
            
            st.divider()
            st.button("🗑️ Hapus Chat", key="clear_btn", on_click=hapus_obrolan)

    with col_input:
        st.text_input(
            "", 
            placeholder="Tanyakan apa saja", 
            key="input_box", 
            label_visibility="collapsed",
            on_change=kirim_pesan
        )

    with col_send:
        st.button("🚀", key="send_btn", on_click=kirim_pesan)
        
    st.markdown('</div>', unsafe_allow_html=True)
