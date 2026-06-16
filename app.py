import streamlit as st
import google.generativeai as genai
import json

# --- CẤU HÌNH ---
st.set_page_config(page_title="The Analytical Journey", layout="centered")

st.title("🗡️ The Analytical Journey")
with st.sidebar:
    st.header("🔑 Connection")
    api_key = st.text_input("Enter your Gemini API Key:", type="password")

if not api_key:
    st.info("👋 **Game Master:** Welcome, brave explorer! I am your mentor. Please enter your API Key in the sidebar to begin our journey.")
    st.stop()

genai.configure(api_key=api_key)

# --- AI ENGINE ---
def call_ai(prompt, is_json=False):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(text) if is_json else text
    except: return None

# --- STATE MANAGEMENT ---
if 'stage' not in st.session_state:
    st.session_state.stage = 0
    st.session_state.answers = {}

# TRẠM 0: NHẬP ĐỀ
if st.session_state.stage == 0:
    st.write("📖 **Game Master:** Tell me your IELTS topic, and I will prepare your analytical path.")
    topic = st.text_area("Topic:", key="topic_input")
    if st.button("🚀 Begin Your Journey"):
        if topic:
            with st.spinner("Game Master is building your quest..."):
                prompt = f"Topic: '{topic}'. Act as a mentor. Create 3 RPG roles: 1.Individual, 2.Organization, 3.Government. Give 1 guiding question for each. Return ONLY JSON: {{\"micro\": {{\"role\": \"\", \"question\": \"\"}}, \"meso\": {{\"role\": \"\", \"question\": \"\"}}, \"macro\": {{\"role\": \"\", \"question\": \"\"}}}}"
                roles = call_ai(prompt, True)
                if roles:
                    st.session_state.roles = roles
                    st.session_state.topic = topic
                    st.session_state.stage = 1
                    st.rerun()

# TRẠM 1-3: RPG
elif st.session_state.stage <= 3:
    map_data = {1: ('micro', '🏕️', 'Individual'), 2: ('meso', '🏛️', 'Organization'), 3: ('macro', '🏰', 'Government')}
    key, icon, title = map_data[st.session_state.stage]
    
    st.subheader(f"{icon} {title} Stage")
    st.write(f"**Game Master:** As {st.session_state.roles[key]['role']}, {st.session_state.roles[key]['question']}")
    
    ans = st.text_area("Your thoughts:", key=f"ans_{key}")
    if st.button("Submit & Proceed ➡️"):
        st.session_state.answers[key] = ans
        st.session_state.stage += 1
        st.rerun()

# KẾT QUẢ
elif st.session_state.stage == 4:
    st.balloons()
    st.header("💎 The Treasure Board")
    st.write("Here is your logical mindmap:")
    prompt = f"Topic: {st.session_state.topic}. Analysis: Individual:{st.session_state.answers['micro']}, Organization:{st.session_state.answers['meso']}, Government:{st.session_state.answers['macro']}. Create an IELTS Tree Diagram using '->' to show the flow of ideas."
    st.markdown(call_ai(prompt))
    if st.button("🔄 Restart Journey"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
