import streamlit as st
import google.generativeai as genai
import json

st.set_page_config(page_title="The Analytical Journey", layout="centered")

# --- UI: CONFIG & WELCOME ---
st.title("🗡️ The Analytical Journey")
with st.sidebar:
    st.header("🔑 Connection")
    api_key = st.text_input("Enter your Gemini API Key:", type="password")

if not api_key:
    st.info("👋 **Game Master:** Welcome, brave explorer! I am your mentor. Please enter your API Key in the sidebar to begin our quest.")
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

# --- GAME STATE ---
if 'stage' not in st.session_state:
    st.session_state.stage = 0
    st.session_state.answers = {}

# TRẠM 0: NHẬP ĐỀ
if st.session_state.stage == 0:
    st.write("📖 **Game Master:** Please provide an IELTS Writing Task 2 topic. I will create a quest for you.")
    if topic := st.text_area("Topic:"):
        if st.button("🚀 Start Quest"):
            with st.spinner("Game Master is analyzing..."):
                prompt = f"Topic: '{topic}'. Act as a mentor. Create 3 RPG roles (Micro, Meso, Macro) with 1 guiding question each. Return ONLY JSON: {{\"micro\": {{\"role\": \"\", \"question\": \"\"}}, \"meso\": {{\"role\": \"\", \"question\": \"\"}}, \"macro\": {{\"role\": \"\", \"question\": \"\"}}}}"
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
    
    if ans := st.text_area("Your thoughts (Vietnamese or English):", key=f"ans_{key}"):
        if st.button("Submit & Proceed ➡️"):
            st.session_state.answers[key] = ans
            st.session_state.stage += 1
            st.rerun()

# KẾT QUẢ
elif st.session_state.stage == 4:
    st.balloons()
    st.header("💎 The Treasure Board (Mindmap)")
    prompt = f"Topic: {st.session_state.topic}. Synthesis: Individual={st.session_state.answers['micro']}, Org={st.session_state.answers['meso']}, Gov={st.session_state.answers['macro']}. Create an IELTS Tree Diagram (use arrows ->) showing the logical flow from Individual to Gov."
    st.markdown(call_ai(prompt))
    if st.button("🔄 Restart"):
        st.session_state.clear()
        st.rerun()
