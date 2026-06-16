import streamlit as st
import google.generativeai as genai
import json
import requests
from streamlit_lottie import st_lottie

# --- CẤU HÌNH ---
API_KEY = "YOUR_API_KEY_HERE"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="The Analytical Journey", layout="centered")

@st.cache_data
def load_lottie(url):
    try:
        r = requests.get(url, timeout=3)
        return r.json() if r.status_code == 200 else None
    except: return None

# --- KHỞI TẠO ---
if 'stage' not in st.session_state:
    st.session_state.stage = 0
    st.session_state.roles = None

def get_ai_data(prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(text)
    except Exception as e:
        st.error(f"AI Error: {e}")
        return None

# --- GIAO DIỆN ---
st.title("🗡️ The Analytical Journey")

if st.session_state.stage == 0:
    st.info("Nhập đề bài IELTS Writing Task 2:")
    topic = st.text_area("Topic:")
    if st.button("Bắt đầu"):
        with st.spinner("Đang khởi tạo vai diễn..."):
            roles = get_ai_data(f"Topic: '{topic}'. Create 3 RPG roles (Micro, Meso, Macro) with 1 question each. Return ONLY JSON: {{'micro': {{'role': '', 'question': ''}}, 'meso': {{'role': '', 'question': ''}}, 'macro': {{'role': '', 'question': ''}}}}")
            if roles:
                st.session_state.roles = roles
                st.session_state.topic = topic
                st.session_state.stage = 1
                st.rerun()

elif st.session_state.stage == 1:
    st.subheader(f"🏕️ {st.session_state.roles['micro']['role']}")
    st.write(st.session_state.roles['micro']['question'])
    ans = st.text_area("Trả lời:")
    if st.button("Gửi"):
        st.session_state.micro_ans = ans
        st.session_state.stage = 2
        st.rerun()

elif st.session_state.stage == 2:
    st.subheader(f"🏛️ {st.session_state.roles['meso']['role']}")
    st.write(st.session_state.roles['meso']['question'])
    ans = st.text_area("Trả lời:")
    if st.button("Gửi"):
        st.session_state.meso_ans = ans
        st.session_state.stage = 3
        st.rerun()

elif st.session_state.stage == 3:
    st.subheader(f"🏰 {st.session_state.roles['macro']['role']}")
    st.write(st.session_state.roles['macro']['question'])
    ans = st.text_area("Trả lời:")
    if st.button("Tổng kết"):
        st.session_state.macro_ans = ans
        st.session_state.stage = 4
        st.rerun()

elif st.session_state.stage == 4:
    st.balloons()
    st.header("💎 Dàn ý sơ đồ cây")
    prompt = f"Topic: {st.session_state.topic}. Synthesis ideas: Micro:{st.session_state.micro_ans}, Meso:{st.session_state.meso_ans}, Macro:{st.session_state.macro_ans}. Format as a Tree Diagram using arrow keys (->)."
    model = genai.GenerativeModel('gemini-1.5-flash')
    st.markdown(model.generate_content(prompt).text)
