import os
import streamlit as st
from groq import Groq

# Inisialisasi Groq Client
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 1. Konfigurasi Halaman Utama
st.set_page_config(page_title="AI Chat UI Premium", layout="centered")

# 2. Gaya CSS Kustom (Desain Bersih & Elemen Presisi)
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
    
    /* Khusus untuk Menghilangkan Border Default pada Tombol Titik Tiga Transparan */
    div[data-testid="element-container"] .titik-tiga-container button {
        border: none !important;
        background: transparent !important;
        font-size: 24px !important;
        box-shadow: none !important;
    }
    
    /* Kotak Input Teks */
    div[data-testid="stTextInput"] input {
        border-radius: 20px !important;
        height: 46px !important;
        border: 1px solid #e0e0e0 !important;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
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

# 3. Baris Navigasi Atas & Menu Titik Tiga (⋮)
col_nav, col_menu = st.columns([8.5, 1.5], vertical_alignment="center")

with col_nav:
    st.write("✨ **Mode AI** &nbsp;|&nbsp; Semua &nbsp;|&nbsp; Gambar &nbsp;|&nbsp; Video &nbsp;|&nbsp; Berita &nbsp;|&nbsp; Lainnya")

with col_menu:
    # Menu Popover Titik Tiga di Pojok Kanan Atas
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
            if "img_upload" in st.session_state:
                del st.session_state["img_upload"]
            if "file_upload" in st.session_state:
                del st.session_state["file_upload"]
            st.rerun()

st.divider()

# 4. Inisialisasi Memori Percakapan
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan Riwayat Chat Ke Layar
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
            system_instruction = opsi_bahasa[bahasa_terpilih]
            history = [{"role": "system", "content": system_instruction}]
            history.extend([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages])
            
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=history
            )
            st.session_state.messages.append({"role": "assistant", "content": completion.choices[0].message.content})
        except Exception as e:
            st.session_state.messages.append({"role": "assistant", "content": f"Gagal memproses: {e}"})
        
        st.session_state["input_box"] = ""

# 6. Baris Menu Aksi & Kotak Input Bawah (Desain Presisi Multi-Kategori)
st.write("") 
col_popover, col_input, col_send = st.columns([1.5, 7, 1.5], vertical_alignment="bottom")

with col_popover:
    with st.popover("➕"):
        # KELOMPOK 1: MENU UNGGAH
        st.caption("📎 **Upload & Lampiran**")
        st.file_uploader("📂 Upload file teks/dokumen", type=["txt", "pdf"], key="file_upload")
        st.file_uploader("📸 Upload gambar/foto", type=["png", "jpg", "jpeg"], key="img_upload")
        
        st.divider()
        
        # KELOMPOK 2: MENU ALAT KREASI
        st.caption("🤖 **Alat & Kreasi AI**")
        if st.button("🎨 Buat gambar (Baru)", use_container_width=True):
            st.toast("Fitur Canvas/Gambar siap dikembangkan!")
        if st.button("📝 Canvas", use_container_width=True):
            st.toast("Membuka ruang kerja Canvas...")
        if st.button("🔍 Deep Research", use_container_width=True):
            st.toast("Memulai analisis mendalam...")

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
