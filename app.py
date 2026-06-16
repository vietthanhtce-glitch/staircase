import streamlit as st
import google.generativeai as genai
import json

st.set_page_config(page_title="The Analytical Journey", layout="centered")

# --- UI: API KEY ---
st.title("🗡️ The Analytical Journey")
api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")

if not api_key:
    st.info("👋 Game Master: Hello traveler! Please enter your API Key in the sidebar to begin.")
    st.stop()

genai.configure(api_key=api_key)

# --- AI HELPER ---
def get_ai_data(topic):
    # Model 1.5-flash là model nhanh nhất và ổn định nhất cho tài khoản free
    model = genai.GenerativeModel('gemini-1.5-flash')
    # Prompt này ép AI chỉ được làm việc duy nhất là chia 3 vai diễn cho mọi đầu vào
    prompt = f"Topic: '{topic}'. Act as a game mentor. Create 3 RPG roles (Micro, Meso, Macro) based on this topic with 1 guiding question in English for each. Return ONLY a pure JSON object, no other text: {{'micro': {{'role': 'A', 'question': 'B'}}, 'meso': {{'role': 'C', 'question': 'D'}}, 'macro': {{'role': 'E', 'question': 'F'}}}}"
    
    try:
        response = model.generate_content(prompt)
        text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(text)
    except Exception:
        # Nếu AI không ra được JSON chuẩn, ta dùng fallback để game không chết
        return {"micro": {"role": "Individual", "question": "How does this affect you?"}, 
                "meso": {"role": "Organization", "question": "How do you manage this?"}, 
                "macro": {"role": "Society", "question": "What is the global impact?"}}

# --- GAME LOGIC ---
if 'stage' not in st.session_state: st.session_state.stage = 0

if st.session_state.stage == 0:
    topic = st.text_area("Enter your IELTS Topic (Any topic is welcome!):")
    if st.button("🚀 Start Adventure"):
        with st.spinner("Game Master is preparing..."):
            roles = get_ai_data(topic)
            st.session_state.roles = roles
            st.session_state.topic = topic
            st.session_state.stage = 1
            st.rerun()

elif st.session_state.stage <= 3:
    map_data = {1: ('micro', '🏕️', 'Micro Village'), 2: ('meso', '🏛️', 'Meso Guild'), 3: ('macro', '🏰', 'Macro Kingdom')}
    key, icon, title = map_data[st.session_state.stage]
    
    st.subheader(f"{icon} {title}")
    st.write(f"**Game Master:** {st.session_state.roles[key]['question']}")
    
    if ans := st.text_area("Your thoughts:", key=f"ans_{key}"):
        if st.button("Continue ➡️"):
            st.session_state.stage += 1
            st.rerun()

elif st.session_state.stage == 4:
    st.balloons()
    st.header("💎 Final Mindmap")
    st.markdown(f"**Topic:** {st.session_state.topic}\n\n*Great job! Your ideas have been synthesized.*")
    if st.button("🔄 Restart"):
        st.session_state.clear()
        st.rerun()
