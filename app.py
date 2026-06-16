import streamlit as st
import google.generativeai as genai
import json

# --- CẤU HÌNH CỐ ĐỊNH (Không dùng sidebar nữa để tránh rắc rối) ---
# Dán API KEY của bạn vào đây
API_KEY = "DÁN_API_KEY_CỦA_BẠN_VÀO_ĐÂY"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="The Analytical Journey", layout="centered")

# --- HÀM GỌI AI ĐƠN GIẢN NHẤT ---
def get_ai_data(prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(text)
    except Exception as e:
        st.error(f"AI Error: {e}") # Báo rõ lỗi tại sao không chạy được
        return None

# --- GIAO DIỆN ---
st.title("🗡️ The Analytical Journey")

if 'stage' not in st.session_state: st.session_state.stage = 0

if st.session_state.stage == 0:
    st.info("👋 Game Master: Chào bạn! Nhập đề bài IELTS để bắt đầu.")
    if topic := st.text_area("Đề bài:"):
        if st.button("🚀 Bắt đầu"):
            with st.spinner("Đang kết nối..."):
                # Dùng prompt đơn giản nhất để AI không hiểu lầm
                prompt = f"Topic: '{topic}'. Give me 3 roles (Micro, Meso, Macro) with 1 question each. Return ONLY JSON: {{\"micro\": {{\"role\": \"A\", \"question\": \"B\"}}, \"meso\": {{\"role\": \"C\", \"question\": \"D\"}}, \"macro\": {{\"role\": \"E\", \"question\": \"F\"}}}}"
                roles = get_ai_data(prompt)
                if roles:
                    st.session_state.roles = roles
                    st.session_state.topic = topic
                    st.session_state.stage = 1
                    st.rerun()
