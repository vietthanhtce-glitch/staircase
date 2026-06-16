import streamlit as st
import google.generativeai as genai
import json
import requests
from streamlit_lottie import st_lottie

st.set_page_config(page_title="The Analytical Journey", layout="centered")

# --- HÀM HỖ TRỢ ---
def load_lottie(url):
    try:
        r = requests.get(url, timeout=3)
        return r.json() if r.status_code == 200 else None
    except: return None

# --- SIDEBAR: Luôn yêu cầu API KEY ---
with st.sidebar:
    st.header("🔑 Cấu hình kết nối")
    user_api_key = st.text_input("Dán Gemini API Key của bạn vào đây:", type="password")
    st.caption("Game sẽ chỉ bắt đầu khi bạn dán Key hợp lệ.")

# --- KIỂM TRA API KEY ---
if not user_api_key:
    st.title("🗡️ The Analytical Journey")
    st.info("👋 **Game Master:** Chào lữ khách! Hãy cung cấp 'Chìa khóa ma thuật' (API Key) ở cột bên trái để ta bắt đầu cuộc phiêu lưu này nhé!")
    st.stop() # Dừng lại, không chạy tiếp nếu chưa có Key

# Nếu có Key, mới tiếp tục chạy game
genai.configure(api_key=user_api_key)

def get_ai_data(prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        response = model.generate_content(prompt)
        text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(text)
    except Exception as e:
        st.error(f"Lỗi AI: {e}")
        return None

# --- TRẠNG THÁI GAME ---
if 'stage' not in st.session_state:
    st.session_state.stage = 0

st.title("🗡️ The Analytical Journey")

# --- TRẠM 0: CHÀO HỎI ---
if st.session_state.stage == 0:
    st.info("👋 **Game Master:** Chào mừng bạn! Hãy nhập đề bài IELTS Writing Task 2 để ta bắt đầu xây dựng chiến lược nhé!")
    topic = st.text_area("Nhập đề bài:")
    if st.button("🚀 Bắt đầu hành trình"):
        with st.spinner("Game Master đang phân tích đề bài..."):
            roles = get_ai_data(f"Topic: '{topic}'. Create 3 RPG roles (Micro, Meso, Macro) with 1 question each. Return ONLY JSON: {{'micro': {{'role': '', 'question': ''}}, 'meso': {{'role': '', 'question': ''}}, 'macro': {{'role': '', 'question': ''}}}}")
            if roles:
                st.session_state.roles = roles
                st.session_state.topic = topic
                st.session_state.stage = 1
                st.rerun()
            else:
                st.error("AI không thể kết nối. Hãy kiểm tra API Key của bạn!")

# [GIỮ NGUYÊN CÁC STAGE 1, 2, 3, 4 NHƯ ĐOẠN CODE TRƯỚC]
# (Nếu bạn cần tôi dán lại toàn bộ từ A-Z một lần nữa, hãy bảo tôi nhé!)
