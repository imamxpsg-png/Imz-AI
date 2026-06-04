import os
import streamlit as st
from groq import Groq

# Inisialisasi Groq Client
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 1. Konfigurasi Halaman Utama
st.set_page_config(page_title="Imz-AI Mobile", layout="centered")

# 2. Gaya CSS Kustom - Desain Kapsul Menyatu Terpadu (Mobile-First)
st.markdown("""
    <style>
    /* Mengurangi margin default Streamlit agar area chat luas di HP */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* ANIMASI WARNA BERJALAN UNTUK JUDUL ATAS */
    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .animated-title {
        font-size: 28px;
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
    
    /* GAYA TEKS PEMBUKA DI TENGAH LAYAR */
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
        font-size: 16px;
        font-weight: 500;
        color: #4a5568;
        line-height: 1.5;
    }
    
    /* WADAH UTAMA KAPSUL INPUT (Menyatukan tombol +, teks, dan kirim) */
    .unified-input-row {
        background-color: #f1f3f4 !important; /* Latar abu-abu menyatu */
        border: 1px solid #e2e8f0 !important;
        border-radius: 24px !important;
        padding: 4px 8px !important;
        display: flex !important;
        align-items: center !important;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.04);
        margin-top: 15px;
    }

    /* Menghilangkan latar belakang putih dan border bawaan kolom teks */
    div[data-testid="stTextInput"] input {
        border: none !important;
        box-shadow: none !important;
        background-color: transparent !important;
        padding-left: 5px !important;
        font-size: 15px !important;
        height: 38px !important;
    }
    
    /* Menghilangkan margin dan celah antar kolom bawaan Streamlit */
    div[data-testid="stColumn"] {
        padding: 0px !important;
        margin: 0px !important;
    }
    div[data-testid="stHorizontalBlock"] {
        align-items: center !important;
        gap: 0px !important; 
    }

    /* Mengubah tombol Popover Plus menjadi menyatu di dalam kotak */
    div[data-testid="stPopover"] {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        background-color: transparent !important; 
        color: #5f6368 !important;
        border: none !important;
        height: 36px !important;
        width: 36px !important;
        min-width: 36px !important;
        box-shadow: none !important;
        padding: 0 !important;
    }
    div[data-testid="stPopover"] > button:hover {
        background-color: rgba(0, 0, 0, 0.05) !important;
    }

    /* Mengubah Tombol Kirim 🚀 menjadi transparan agar menyatu */
    div.stButton {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    div.stButton > button[key="send_btn"] {
        background: transparent !important; 
        color: #1a73e8 !important; 
        font-size: 18px !important;
        border-radius: 50% !important;
        border: none !important;
        height: 36px !important;
        width: 36px !important;
        min-width: 36px !important;
        box-shadow: none !important;
        padding: 0 !important;
    }
    div.stButton > button[key="send_btn"]:hover {
        background-color: rgba(0, 0, 0, 0.05) !important;
    }

    /* Gelembung Chat Responsif Layar HP */
    .bubble-user {
        background-color: #f0f4f9;
        padding: 10px 14px;
        border-radius: 16px 16px 0px 16px;
        margin-bottom: 10px;
        max-width: 90%;
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
    
    /* Tombol Hapus Chat Merah Merona di Popover */
    div.stButton > button[key="clear_btn"] {
        background-color: #ff4b4b !important;
        color: white !important;
        border-radius: 10px;
        border: none;
        width: 100%;
        padding: 8px !important;
    }
    div.stButton > button[key="clear_btn"]:hover {
        background-color: #d93838 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Baris Atas: Judul Utama Beranimasi
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

# Tampilan Konten: Selamat Datang atau Sesi Riwayat Pesan
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
            
            # Membongkar indeks list data respons menggunakan indeks [0] dengan benar
            if completion.choices:
                first_choice = completion.choices[0]
                if hasattr(first_choice, "message"):
                    ai_response = first_choice.message.content if hasattr(first_choice.message, "content") else first_choice.message["content"]
                else:
                    ai_response = first_choice["message"]["content"]
            else:
                ai_response = "Maaf, tidak ada respon yang diterima dari sistem AI."
                
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        except Exception as e:
            st.session_state.messages.append({"role": "assistant", "content": f"Gagal memproses: {e}"})
        
        st.session_state["input_box"] = ""

def hapus_obrolan():
    st.session_state.messages = []
    if "img_upload" in st.session_state:
        del st.session_state["img_upload"]
    if "file_upload" in st.session_state:
        del st.session_state["file_upload"]

# 6. PANEL INPUT UTAMA: Kontainer HTML Terpadu (.unified-input-row)
st.write("") 
st.markdown('<div class="unified-input-row">', unsafe_allow_html=True)

# Memisahkan baris kapsul menjadi 3 kolom mikro (Proporsional HP)
col_popover, col_input, col_send = st.columns([1.3, 7.4, 1.3], vertical_alignment="center")

with col_popover:
    with st.popover("＋"):
        st.caption("📂 **Lampiran & Berkas**")
        st.file_uploader("🖼️ Upload gambar", type=["png", "jpg", "jpeg"], key="img_upload")
        st.file_uploader("📄 Upload file", type=["txt", "pdf"], key="file_upload")
        
        st.divider()
        st.caption("🎨 **Alat Kreatif**")
        if st.button("Buat gambar", use_container_width=True):
            st.toast("Fitur generator siap dihubungkan!")
            
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
