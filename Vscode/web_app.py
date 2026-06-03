import os
import streamlit as st
from groq import Groq

# Ganti baris inisialisasi API Key kamu menjadi seperti ini:
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 1. Pengaturan Halaman Utama
st.set_page_config(page_title="Asisten AI Premium", page_icon="🤖", layout="centered")

# 2. Desain Tampilan Cerah & Bersih (Light Theme)
st.markdown("""
    <style>
    /* Background Gambar Hokkaido */
    .stApp {
        background-image: url("https://i.pinimg.com/1200x/eb/70/5d/eb705dc1184fe975d8fa496121dcecdb.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Overlay Putih Transparan (Cerah & Bersih) */
    .block-container {
        background-color: rgba(255, 255, 255, 0.94);
        padding: 40px !important;
        border-radius: 20px;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.15);
        margin-top: 30px;
    }
    
    h1 {
        color: #1e3c72;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }
    
    .marquee-text {
        font-weight: bold;
        color: #d9534f;
        font-size: 16px;
    }

    /* Gaya Bubble Chat Gaya WhatsApp/ChatGPT */
    .chat-bubble-user {
        background-color: #e2f0cb;
        color: #111111 !important;
        padding: 12px 18px;
        border-radius: 15px 15px 0px 15px;
        margin-bottom: 15px;
        text-align: right;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
    }
    
    .chat-bubble-ai {
        background-color: #f1f3f5;
        color: #111111 !important;
        padding: 12px 18px;
        border-radius: 15px 15px 15px 0px;
        margin-bottom: 15px;
        text-align: left;
        max-width: 80%;
        margin-right: auto;
        border-left: 4px solid #4facfe;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
    }

    /* Kustomisasi Tombol "+" */
    div.stButton > button[key="plus_btn"] {
        border-radius: 10px !important;
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #ccc !important;
        height: 45px;
        width: 45px;
    }

    /* Kustomisasi Tombol Kirim Utama */
    div.stButton > button:not([key="plus_btn"]) {
        background: linear-gradient(45deg, #00f2fe 0%, #4facfe 100%);
        color: white !important;
        font-size: 16px;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 25px;
        border: none;
        box-shadow: 0px 4px 15px rgba(0, 242, 254, 0.2);
        transition: all 0.3s ease-in-out;
        width: 100%;
        height: 45px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Judul Aplikasi & Teks Berjalan
st.title("🤖 Aplikasi Chat AI Premium")
st.markdown('<marquee class="marquee-text">Selamat datang di Aplikasi AI Berkelanjutan! Ketik pertanyaan apa saja dan AI akan mengingat obrolan Anda sebelumnya.</marquee>', unsafe_allow_html=True)

# 4. Inisialisasi Memori Riwayat Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan semua riwayat chat dari memori ke layar
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-bubble-user'><b>Anda:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f"<div class='chat-bubble-ai'><b>AI:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

st.write("---")

# 5. Fungsi Callback untuk Menghapus Kolom Input Otomatis setelah Kirim
def proses_kirim():
    # Mengambil teks pertanyaan dari state input_box
    pertanyaan_user = st.session_state.input_box
    
    if pertanyaan_user.strip() != "":
        # Membaca isi file jika ada lampiran teks
        konteks_file = ""
        if st.session_state.get('file_uploader_key') is not None:
            file_konten = st.session_state.file_uploader_key
            konteks_file = f"\n\n[Isi file lampiran: {file_konten.read().decode('utf-8')}]"

        # Simpan pertanyaan ke memori chat
        st.session_state.messages.append({"role": "user", "content": pertanyaan_user + konteks_file})

        try:
            # Ambil respons dari Groq AI
            payload_pesan = [{"role": "system", "content": "Anda adalah asisten AI ramah yang menjawab dalam bahasa Indonesia."}]
            payload_pesan.extend(st.session_state.messages)

            respons = client.chat.completions.create(
                model="llama-3.1-8b-instant", 
                messages=payload_pesan
            )
            
            # Memperbaiki pembacaan indeks list model Groq
            jawaban_ai = respons.choices[0].message.content
            
            # Simpan jawaban AI ke memori chat
            st.session_state.messages.append({"role": "assistant", "content": jawaban_ai})

        except Exception as e:
            st.session_state.messages.append({"role": "assistant", "content": f"Terjadi kesalahan sistem: {e}"})
            
    # PENTING: Mengosongkan teks di kotak input secara otomatis setelah proses selesai
    st.session_state.input_box = ""

# 6. BARIS INPUT MODERN
if "status_upload" not in st.session_state:
    st.session_state.status_upload = False

col_plus, col_txt, col_send = st.columns([1, 8, 2])

with col_plus:
    buka_upload = st.button("➕", key="plus_btn", help="Klik untuk unggah file/foto")
    if buka_upload:
        st.session_state.status_upload = not st.session_state.status_upload

with col_txt:
    st.text_input("", placeholder="Tanyakan apa saja ke AI...", key="input_box", label_visibility="collapsed")

with col_send:
    # Tombol kirim memicu fungsi callback yang sama
    st.button("Kirim 🚀", on_click=proses_kirim)

# 7. Panel Tempat Mengunggah File
if st.session_state.status_upload:
    st.markdown("<div style='background-color: #f1f3f5; padding: 15px; border-radius: 15px; border: 1px dashed #4facfe; margin-top: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        foto_diunggah = st.file_uploader("📸 Tambah Foto", type=["png", "jpg", "jpeg"])
        if foto_diunggah:
            st.image(foto_diunggah, width=100)
    with c2:
        st.file_uploader("📁 Tambah File Teks (TXT)", type=["txt"], key="file_uploader_key")
    st.markdown("</div>", unsafe_allow_html=True)
