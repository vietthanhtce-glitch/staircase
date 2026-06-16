import streamlit as st
import google.generativeai as genai
import json
import requests
from streamlit_lottie import st_lottie

# --- CẤU HÌNH API ---
API_KEY = "YOUR_API_KEY_HERE" # Dán Key của bạn vào đây
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="The Analytical Journey", page_icon="🗡️", layout="centered")

# --- HÀM HỖ TRỢ ---
@st.cache_data
def load_lottie(url):
    try:
        r = requests.get(url, timeout=3)
        return r.json() if r.status_code == 200 else None
    except: return None

# Animation nhân vật
lottie_char = load_lottie("https://assets10.lottiefiles.com/packages/lf20_q7uarxsb.json")

def get_ai_response(prompt, is_json=False):
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        response = model.generate_content(prompt)
        text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(text) if is_json else text
    except: return None

# --- GIAO DIỆN ---
st.title("🗡️ The Analytical Journey")
st.markdown("---")

if 'stage' not in st.session_state:
    st.session_state.stage = 0
    st.session_state.history = []

# STAGE 0: KHỞI ĐỘNG
if st.session_state.stage == 0:
    if lottie_char: st_lottie(lottie_char, height=150)
    st.info("👋 **Game Master:** Hello explorer! I'm your travel companion. Give me an IELTS topic, and let's turn it into a quest!")
    if topic := st.text_area("Enter your topic here:"):
        if st.button("🚀 Let's Go!"):
            with st.spinner("Preparing your quest..."):
                roles = get_ai_data = get_ai_response(f"Topic: '{topic}'. Create 3 RPG roles (Micro, Meso, Macro) with 1 engaging question each. Return ONLY JSON: {{'micro': {{'role': '', 'question': ''}}, 'meso': {{'role': '', 'question': ''}}, 'macro': {{'role': '', 'question': ''}}}}", True)
                if roles:
                    st.session_state.roles = roles
                    st.session_state.topic = topic
                    st.session_state.stage = 1
                    st.rerun()

# CÁC STAGE CHƠI (Dùng Chat Interface)
elif st.session_state.stage <= 3:
    stages = {1: ('micro', '🏕️', 'Micro Village'), 2: ('meso', '🏛️', 'Meso Guild'), 3: ('macro', '🏰', 'Macro Kingdom')}
    s = st.session_state.stage
    key, icon, title = stages[s]
    
    st.subheader(f"{icon} {title}")
    st.chat_message("assistant").write(f"You are now acting as: **{st.session_state.roles[key]['role']}**\n\n{st.session_state.roles[key]['question']}")
    
    if ans := st.chat_input("Share your thoughts (Vietnamese/English):"):
        st.chat_message("user").write(ans)
        # Lưu câu trả lời
        setattr(st.session_state, f"{key}_ans", ans)
        
        # Feedback thân thiện
        fb = get_ai_response(f"As a friendly guide, acknowledge user input '{ans}' (as {st.session_state.roles[key]['role']}). Suggest 3 relevant IELTS vocabulary items. Use emojis! Short & sweet.")
        st.chat_message("assistant").write(fb)
        
        if st.button("Continue the journey ➡️"):
            st.session_state.stage += 1
            st.rerun()

# STAGE 4: TỔNG KẾT
elif st.session_state.stage == 4:
    st.balloons()
    st.header("💎 The Treasure Board")
    st.write("Game Master has forged your ideas into a logical Tree Diagram:")
    
    prompt = f"""
    Topic: {st.session_state.topic}
    Ideas: Micro: {st.session_state.micro_ans}, Meso: {st.session_state.meso_ans}, Macro: {st.session_state.macro_ans}
    
    Create a detailed Tree Diagram using this structure:
    ### 🌳 {st.session_state.topic}
    * 🏕️ Micro: [Key ideas] -> [Vocab]
    * 🏛️ Meso: [Key ideas] -> [Vocab]
    * 🏰 Macro: [Key ideas] -> [Vocab]
    
    Use arrows '->' to show logical flow.
    """
    st.markdown(get_ai_response(prompt))
    if st.button("🔄 Restart"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
