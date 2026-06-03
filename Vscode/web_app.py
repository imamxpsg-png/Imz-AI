import os
import streamlit as st
from groq import Groq

# 1. Konfigurasi Halaman Utama
st.set_page_config(page_title="AI Chat UI Premium", layout="centered")

# Inisialisasi Groq Client
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 2. Gaya CSS Kustom (Efek Cahaya, Bubble Chat, Menyembunyikan Kotak Upload)
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* GAYA TEKS PEMBUKA DI TENGAH LAYAR */
    .welcome-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 35vh;
        text-align: center;
        margin-bottom: 20px;
    }
    .welcome-text {
        font-size: 34px;
        font-weight: 500;
        color: #1f1f1f;
        background: linear-gradient(45deg, #1e3c72, #2a5298);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.4;
    }
    
    /* Sembunyikan Kotak UI Upload Bawaan Streamlit agar langsung memicu folder saja */
    div[data-testid="stFileUploader"] section {
        display: none !important;
    }
    div[data-testid="stFileUploader"] {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Tombol Popover Aksi (+) */
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

    div[data-testid="stTextInput"] input {
        border-radius: 20px !important;
        height: 46px !important;
        border: 2px solid #e0e0e0 !important;
        animation: borderGlow 6s linear infinite;
        transition: all 0.3s ease;
    }

    /* Tombol Kirim Tanda Panah (⬆) */
    div.stButton > button[key="send_btn"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        font-size: 18px !important;
        font-weight: bold;
        border-radius: 50% !important;
        border: none;
        height: 46px;
        width: 46px;
        min-width: 46px;
        max-width: 46px;
        padding: 0 !important;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0px 4px 10px rgba(118, 75, 162, 0.2);
    }

    /* Kustomisasi tombol menu dalam Popover */
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
        height: auto !important;
        width: 100% !important;
    }
    div[data-testid="stPopover"] div.stButton > button:hover {
        background-color: #f5f5f5 !important;
    }
    
    div[data-testid="stPopover"] div.stButton > button[key="inner_clear_btn"] {
        color: #ff4b4b !important;
        font-weight: bold !important;
    }
    div[data-testid="stPopover"] div.stButton > button[key="inner_clear_btn"]:hover {
        background-color: #ffebe8 !important;
    }

    .bubble-user {
        background-color: #f0f4f9;
        padding: 14px 18px;
        border-radius: 18px 18px 0px 18px;
        margin-bottom: 12px;
        max-width: 85%;
        margin-left: auto;
        color: #202124;
    }

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

# Kamus pilihan bahasa
opsi_bahasa = {
    "Bahasa Indonesia 🇮🇩": "Anda adalah asisten AI ramah yang wajib menjawab dalam Bahasa Indonesia.",
    "English 🇺🇸": "You are a helpful AI assistant. You must respond strictly in English.",
    "Japanese 🇯🇵": "あなたは親切なAIアシスタントです。必ず日本語で答えてください。",
    "Korean 🇰🇷": "당신은 친절한 AI 어시스턴트입니다. 반드시 한국어로 답변해 주세요.",
    "Chinese 🇨🇳": "你是一个友好的AI助手。请务必用中文回答。"
}

# 3. Inisialisasi Memori Percakapan & State Aksi
if "messages" not in st.session_state:
    st.session_state.messages = []
if "menu_action" not in st.session_state:
    st.session_state.menu_action = None
if "bahasa_sekarang" not in st.session_state:
    st.session_state.bahasa_sekarang = "Bahasa Indonesia 🇮🇩"

# 4. LOGIKA TAMPILAN KONTEN CHAT / SAPAAN TENGAH
if not st.session_state.messages:
    st.markdown(
        '<div class="welcome-container"><h1 class="welcome-text">Halo, apa ada hal yang bisa dibantu?</h1></div>', 
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
    
    # Kumpulkan lampiran tersembunyi jika ada yang berhasil diunggah
    lampiran_konteks = ""
    if st.session_state.get("hidden_img"):
        lampiran_konteks += f" [*Menerima lampiran gambar: {st.session_state.hidden_img.name}*]"
    if st.session_state.get("hidden_file"):
        lampiran_konteks += f" [*Menerima lampiran dokumen: {st.session_state.hidden_file.name}*]"

    if user_text or lampiran_konteks:
        st.session_state.messages.append({"role": "user", "content": user_text + lampiran_konteks})
        try:
            system_instruction = opsi_bahasa[st.session_state.bahasa_sekarang]
            history = [{"role": "system", "content": system_instruction}]
            history.extend([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages])
            
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=history
            )
            st.session_state.messages.append({"role": "assistant", "content": completion.choices[0].message.content})
        except Exception as e:
            st.session_state.messages.append({"role": "assistant", "content": f"Gagal memproses: {e}"})
        
        # Reset input setelah terkirim
        st.session_state["input_box"] = ""

def set_action(action_name):
    st.session_state.menu_action = action_name

# 6. PENAMPUNG PROSES UPLOAD TERSEMBUNYI (TIDAK TERLIHAT DI UI)
# Peletakan elemen ini mendeteksi perubahan unggahan di latar belakang halaman
uploaded_img = st.file_uploader("", type=["png", "jpg", "jpeg"], key="hidden_img", label_visibility="collapsed")
uploaded_txt = st.file_uploader("", type=["txt", "pdf"], key="hidden_file", label_visibility="collapsed")

# Memunculkan notifikasi kecil (toast) jika berkas masuk lewat background folder
if uploaded_img:
    st.toast(f"📸 Gambar '{uploaded_img.name}' siap dikirim!")
if uploaded_txt:
    st.toast(f"📎 Dokumen '{uploaded_txt.name}' siap dikirim!")

# 7. BARIS BAWAH MINIMALIS (3 Kolom: ➕ | Input Chat | ⬆)
st.write("") 
col_plus, col_input, col_send = st.columns([1.3, 7.4, 1.3], vertical_alignment="bottom")

with col_plus:
    with st.popover("➕"):
        st.caption("📎 **Upload & Lampiran**")
        
        # Memicu pemilih dokumen secara native (HTML) lewat integrasi trik label pengunggah berkas
        st.markdown('<label for="hidden_img-uploader" style="cursor:pointer; display:block; padding:8px 12px; border-radius:8px; font-size:15px; color:#333333;">📸 Upload gambar</label>', unsafe_allow_html=True)
        st.markdown('<label for="hidden_file-uploader" style="cursor:pointer; display:block; padding:8px 12px; border-radius:8px; font-size:15px; color:#333333;">📎 Upload file</label>', unsafe_allow_html=True)
        
        st.divider()
        st.caption("🤖 **Alat AI**")
        st.button("🍌 Buat gambar", use_container_width=True, on_click=set_action, args=("buat_gambar",))
        
        st.divider()
        st.caption("🌐 **Pengaturan Bahasa**")
        st.session_state.bahasa_sekarang = st.selectbox(
            "Pilih Bahasa:",
            options=list(opsi_bahasa.keys()),
            index=list(opsi_bahasa.keys()).index(st.session_state.bahasa_sekarang),
            label_visibility="collapsed"
        )
        
        st.divider()
        st.caption("⚙️ **Manajemen Chat**")
        if st.button("🗑️ Hapus Chat", key="inner_clear_btn", use_container_width=True):
            st.session_state.messages = []
            st.session_state.menu_action = None
            st.rerun()

with col_input:
    st.text_input(
        "", 
        placeholder="Tanya AI...", 
        key="input_box", 
        label_visibility="collapsed",
        on_change=kirim_pesan
    )
                
with col_send:
    st.button("⬆", key="send_btn", on_click=kirim_pesan)
