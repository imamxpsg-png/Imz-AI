import os
import streamlit as st
from groq import Groq

# Inisialisasi Groq Client
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 1. Konfigurasi Halaman Utama
st.set_page_config(page_title="AI Chat UI Premium", layout="centered")

# 2. Gaya CSS Kustom (Efek Cahaya Bergerak & Tombol Menu Presisi)
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Tombol Popover Alat Melayang (+) dan Menu Titik Tiga (⋮) */
    div[data-testid="stPopover"] > button {
        border-radius: 20px !important;
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #e0e0e0 !important;
        height: 46px;
        width: 100%;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    }
    
    /* ANIMASI CAHAYA BERGERAK PADA KOLOM INPUT CHAT */
    @keyframes borderGlow {
        0% { border-color: #ff4fac; box-shadow: 0 0 10px rgba(255, 79, 172, 0.5); }
        33% { border-color: #00f2fe; box-shadow: 0 0 10px rgba(0, 242, 254, 0.5); }
        66% { border-color: #764ba2; box-shadow: 0 0 10px rgba(118, 75, 162, 0.5); }
        100% { border-color: #ff4fac; box-shadow: 0 0 10px rgba(255, 79, 172, 0.5); }
    }

    /* Menerapkan animasi cahaya bergerak pada kotak input teks */
    div[data-testid="stTextInput"] input {
        border-radius: 20px !important;
        height: 46px !important;
        border: 2px solid #e0e0e0 !important;
        animation: borderGlow 6s linear infinite;
        transition: all 0.3s ease;
    }

    /* Tombol Kirim Bundar */
    div.stButton > button[key="send_btn"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        font-weight: bold;
        border-radius: 20px;
        border: none;
        height: 46px;
        width: 100%;
        box-shadow: 0px 4px 10px rgba(118, 75, 162, 0.2);
    }

    /* Kustomisasi gaya tombol di dalam Popover agar teks rata kiri & mirip menu asli */
    div[data-testid="stPopover"] div.stButton > button {
        text-align: left !important;
        justify-content: flex-start !important;
        border: none !important;
        background: transparent !important;
        padding: 8px 12px !important;
        font-size: 15px !important;
        color: #333333 !important;
        box-shadow: none !important;
        border-radius: 8px !important;
    }
    div[data-testid="stPopover"] div.stButton > button:hover {
        background-color: #f5f5f5 !important;
    }

    /* Bubble Chat User */
    .bubble-user {
        background-color: #f0f4f9;
        padding: 14px 18px;
        border-radius: 18px 18px 0px 18px;
        margin-bottom: 12px;
        max-width: 85%;
        margin-left: auto;
        color: #202124;
    }

    /* Bubble Chat AI */
    .bubble-ai {
        background-color: #ffffff;
        padding: 14px 18px;
        border-radius: 18px 18px 18px 0px;
        margin-bottom: 12px;
        max-width: 85%;
        border: 1px solid #e3e3e3;
        color: #202124;
    }
    </style>
""", unsafe_allow_html=True)

# Kamus bahasa beserta instruksi sistem untuk AI
opsi_bahasa = {
    "Bahasa Indonesia 🇮🇩": "Anda adalah asisten AI ramah yang wajib menjawab dalam Bahasa Indonesia.",
    "English 🇺🇸": "You are a helpful AI assistant. You must respond strictly in English.",
    "Japanese 🇯🇵": "あなたは親切なAIアシスタントです。必ず日本語で答えてください。",
    "Korean 🇰🇷": "당신은 친절한 AI 어시스턴트입니다. 반드시 한국어로 답변해 주세요.",
    "Chinese 🇨🇳": "你是一个友好的AI助手。请务必用中文回答。"
}

# 3. BARIS ATAS: MENU TITIK TIGA
col_spacer_top, col_menu = st.columns([8.5, 1.5], vertical_alignment="center")

with col_menu:
    with st.popover("⋮"):
        st.caption("🌐 **Pengaturan Bahasa**")
        bahasa_terpilih = st.selectbox(
            "Pilih Bahasa:",
            options=list(opsi_bahasa.keys()),
            label_visibility="collapsed"
        )
        st.divider()
        st.caption("⚙️ **Aksi Obrolan**")
        if st.button("🗑️ Hapus Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

st.divider()

# 4. Inisialisasi Memori Percakapan & State Aksi
if "messages" not in st.session_state:
    st.session_state.messages = []
if "menu_action" not in st.session_state:
    st.session_state.menu_action = None

# Menampilkan Riwayat Chat Ke Layar
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='bubble-user'><b>Anda:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f"<div class='bubble-ai'><b>AI:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

# 5. Fungsi Eksekusi Pengiriman Pesan (Perbaikan Bug Berhasil)
def kirim_pesan():
    user_text = st.session_state.get("input_box", "").strip()
    if user_text:
        st.session_state.messages.append({"role": "user", "content": user_text})
        try:
            system_instruction = opsi_bahasa[bahasa_terpilih]
            history = [{"role": "system", "content": system_instruction}]
            history.extend([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages])
            
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=history
            )
            # PERBAIKAN: Menambahkan indeks [0] di bawah ini
            st.session_state.messages.append({"role": "assistant", "content": completion.choices[0].message.content})
        except Exception as e:
            st.session_state.messages.append({"role": "assistant", "content": f"Gagal memproses: {e}"})
        st.session_state["input_box"] = ""

# Callback untuk mengubah state tombol menu ➕
def set_action(action_name):
    st.session_state.menu_action = action_name

# 6. PANEL KONDISIONAL UNTUK UPLOAD
if st.session_state.menu_action == "gambar":
    st.file_uploader("🖼 *Pilih file gambar Anda (PNG, JPG):*", type=["png", "jpg", "jpeg"])
    if st.button("❌ Tutup Panel"): set_action(None); st.rerun()
elif st.session_state.menu_action == "file":
    st.file_uploader("📄 *Pilih berkas dokumen Anda (TXT, PDF):*", type=["txt", "pdf"])
    if st.button("❌ Tutup Panel"): set_action(None); st.rerun()
elif st.session_state.menu_action == "buat_gambar":
    st.info("🎨 Fitur Pembuatan Gambar Diaktifkan!")
    if st.button("❌ Tutup Panel"): set_action(None); st.rerun()

# 7. Baris Menu Aksi & Kotak Input Bawah
st.write("") 
col_popover, col_input, col_send = st.columns([1.5, 7, 1.5], vertical_alignment="bottom")

with col_popover:
    with st.popover("➕"):
        st.button("📸 Upload gambar", use_container_width=True, on_click=set_action, args=("gambar",))
        st.button("📎 Upload file", use_container_width=True, on_click=set_action, args=("file",))
        
        st.caption("Alat")
        st.button("🍌 Buat gambar", use_container_width=True, on_click=set_action, args=("buat_gambar",))

with col_input:
    st.text_input(
        "", 
        placeholder="Tanya AI...", 
        key="input_box", 
        label_visibility="collapsed",
        on_change=kirim_pesan
    )

with col_send:
    st.button("🚀", key="send_btn", on_click=kirim_pesan)
