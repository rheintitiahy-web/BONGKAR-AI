import streamlit as st
import google.generativeai as genai

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="BONGKAR - Kab. Sorong Selatan", page_icon="🏗️")

# 2. KEAMANAN API KEY
try:
    # Memanggil kunci dari Streamlit Secrets
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("API Key belum terpasang di Secrets Streamlit!")
    st.stop()

# 3. SETTING MODEL (GEMINI)
# Menggunakan format simpel untuk menghindari error 404 (v1beta)
system_instruction = (
    "Kamu adalah asisten AI resmi untuk aplikasi BONGKAR (Basis Online Navigasi Gerakan Konsultasi Akses Rakyat). "
    "Tugasmu membantu masyarakat Sorong Selatan terkait informasi Dinas PUPR. "
    "Gunakan bahasa yang sopan, solutif, dan profesional. "
    "Aplikasi ini dikembangkan oleh Rain."
)

model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction=system_instruction
)

# 4. TAMPILAN SIDEBAR
with st.sidebar:
    st.title("🏗️ BONGKAR")
    st.subheader("Kab. Sorong Selatan")
    st.write("---")
    st.caption("Dikembangkan oleh: Rain")
    st.info("Aplikasi ini merupakan wadah konsultasi akses rakyat untuk navigasi pelayanan publik.")

# 5. TAMPILAN UTAMA (CHAT)
st.title("Pusat Konsultasi Digital")
st.write("Silakan ajukan pertanyaan Anda seputar layanan PUPR.")

# Inisialisasi riwayat chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan chat lama
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input user
if prompt := st.chat_input("Ketik pertanyaan Anda di sini..."):
    # Simpan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respon AI
    with st.chat_message("assistant"):
        try:
            # Memulai chat tanpa 'model_name=' untuk stabilitas API
            chat = model.start_chat()
            response = chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Terjadi kesalahan teknis: {e}")

st.markdown("---")
st.caption("© 2026 BONGKAR - Basis Online Navigasi Gerakan Konsultasi Akses Rakyat.")
