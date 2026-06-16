import streamlit as st
import google.generativeai as genai
import json
import requests
from streamlit_lottie import st_lottie

# --- CẤU HÌNH ---
API_KEY = "YOUR_API_KEY_HERE" # Dán lại Key vào đây
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="The Analytical Journey", layout="centered")

def load_lottie(url):
    try:
        r = requests.get(url, timeout=3)
        return r.json() if r.status_code == 200 else None
    except: return None

# --- KHỞI TẠO ---
if 'stage' not in st.session_state:
    st.session_state.stage = 0
    st.session_state.topic = ""
    st.session_state.roles = None

# --- HÀM GỌI AI ---
def get_ai_data(prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        response = model.generate_content(prompt)
        text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(text)
    except: return None

# --- GIAO DIỆN ---
st.title("🗡️ The Analytical Journey")

if st.session_state.stage == 0:
    st_lottie(load_lottie("https://assets10.lottiefiles.com/packages/lf20_q7uarxsb.json"), height=150)
    topic = st.text_area("Enter your topic here:")
    
    # Dùng nút bấm để kích hoạt luồng
    if st.button("🚀 Let's Go!"):
        if topic:
            with st.spinner("Game Master is preparing your quest..."):
                roles = get_ai_data(f"Topic: '{topic}'. Create 3 RPG roles (Micro, Meso, Macro) with 1 question each. Return ONLY JSON: {{'micro': {{'role': '', 'question': ''}}, 'meso': {{'role': '', 'question': ''}}, 'macro': {{'role': '', 'question': ''}}}}")
                if roles:
                    st.session_state.roles = roles
                    st.session_state.topic = topic
                    st.session_state.stage = 1
                    st.rerun() # Lệnh này cực quan trọng để ép màn hình tải lại
                else:
                    st.error("AI couldn't start. Please check your API Key permissions!")

elif st.session_state.stage == 1:
    st.subheader("🏕️ Micro Village")
    st.info(f"As {st.session_state.roles['micro']['role']}: {st.session_state.roles['micro']['question']}")
    if ans := st.text_area("Your thoughts:", key="a1"):
        if st.button("Continue"):
            st.session_state.micro_ans = ans
            st.session_state.stage = 2
            st.rerun()

elif st.session_state.stage == 2:
    st.subheader("🏛️ Meso Guild")
    st.info(f"As {st.session_state.roles['meso']['role']}: {st.session_state.roles['meso']['question']}")
    if ans := st.text_area("Your strategy:", key="a2"):
        if st.button("Continue"):
            st.session_state.meso_ans = ans
            st.session_state.stage = 3
            st.rerun()

elif st.session_state.stage == 3:
    st.subheader("🏰 Macro Kingdom")
    st.info(f"As {st.session_state.roles['macro']['role']}: {st.session_state.roles['macro']['question']}")
    if ans := st.text_area("Your policy:", key="a3"):
        if st.button("Show Treasure"):
            st.session_state.macro_ans = ans
            st.session_state.stage = 4
            st.rerun()

elif st.session_state.stage == 4:
    st.balloons()
    st.header("💎 Final Mindmap")
    prompt = f"Topic: {st.session_state.topic}. Ideas: Micro:{st.session_state.micro_ans}, Meso:{st.session_state.meso_ans}, Macro:{st.session_state.macro_ans}. Create a Tree Diagram (using arrow ->) of keywords & vocab."
    model = genai.GenerativeModel('gemini-1.5-flash')
    st.markdown(model.generate_content(prompt).text)
    if st.button("Restart"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
