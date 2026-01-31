import streamlit as st
import google.generativeai as genai

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="BONGKAR - Kab. Sorong Selatan",
    page_icon="🏗️",
    layout="centered"
)

# 2. KEAMANAN API KEY
# Pastikan Anda memasukkan API Key di "Advanced Settings" > "Secrets" di Streamlit Cloud
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("API Key belum terpasang di Secrets Streamlit!")
    st.stop()

# 3. SETTING MODEL (GEMINI)
# Memberikan instruksi agar AI paham tugasnya di aplikasi BONGKAR
system_instruction = (
    "Kamu adalah asisten AI resmi untuk aplikasi BONGKAR (Basis Online Navigasi Gerakan Konsultasi Akses Rakyat). "
    "Tugasmu membantu masyarakat Sorong Selatan terkait informasi Dinas PUPR. "
    "Gunakan bahasa yang sopan, solutif, dan profesional. "
    "Aplikasi ini dikembangkan oleh Rain."
)
model = genai.GenerativeModel(
    model_name='models/gemini-1.5-flash',
    system_instruction=system_instruction
)

# 4. TAMPILAN SIDEBAR
with st.sidebar:
    st.title("🏗️ BONGKAR")
    st.subheader("Kab. Sorong Selatan")
    st.write("---")
    st.write(f"👋 Halo, Rain!")
    st.info(
        "Basis - Online - Navigasi - Gerakan - "
        "Konsultasi - Akses - Rakyat"
    )
    if st.button("Hapus Riwayat Chat"):
        st.session_state.messages = []
        st.rerun()

# 5. TAMPILAN UTAMA
st.title("Pusat Konsultasi Rakyat")
st.caption("Silakan ajukan pertanyaan seputar layanan infrastruktur dan perizinan.")

# Inisialisasi Riwayat Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan Riwayat Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input dari Pengguna
if prompt := st.chat_input("Ketik pertanyaan Anda di sini..."):
    # Simpan chat user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respon AI
    with st.chat_message("assistant"):
        with st.spinner("BONGKAR sedang berpikir..."):
            try:
                # Mengirim seluruh riwayat chat agar AI punya konteks
                full_chat = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                response = model.generate_content(prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

# 6. FOOTER
st.markdown("---")
st.caption("© 2026 BONGKAR. Dikembangkan oleh Rain - Dinas PUPR Sorong Selatan.")
