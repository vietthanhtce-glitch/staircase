import streamlit as st
import google.generativeai as genai
import json

st.set_page_config(page_title="The Analytical Journey", layout="centered")

# --- UI: Yêu cầu nhập Key ---
st.title("🗡️ The Analytical Journey")
api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")

if not api_key:
    st.info("👋 Hello! I'm your Game Master. Please enter your API Key in the sidebar to start our quest.")
    st.stop()

genai.configure(api_key=api_key)

# --- AI Helper ---
def get_ai_response(prompt, is_json=False):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(text) if is_json else text
    except Exception as e:
        return f"Error: {str(e)}"

# --- Logic Game ---
if 'stage' not in st.session_state:
    st.session_state.stage = 0

if st.session_state.stage == 0:
    topic = st.text_area("Enter your IELTS Topic:")
    if st.button("Start Quest"):
        with st.spinner("Game Master is preparing..."):
            prompt = f"Topic: '{topic}'. Act as a mentor. Create 3 RPG roles (Micro, Meso, Macro) with 1 question each in English. Return ONLY JSON: {{\"micro\": {{\"role\": \"\", \"question\": \"\"}}, \"meso\": {{\"role\": \"\", \"question\": \"\"}}, \"macro\": {{\"role\": \"\", \"question\": \"\"}}}}"
            roles = get_ai_response(prompt, True)
            if isinstance(roles, dict):
                st.session_state.roles = roles
                st.session_state.topic = topic
                st.session_state.stage = 1
                st.rerun()
            else:
                st.error("Please enter a valid topic.")

elif st.session_state.stage <= 3:
    map_data = {1: ('micro', '🏕️', 'Micro Village'), 2: ('meso', '🏛️', 'Meso Guild'), 3: ('macro', '🏰', 'Macro Kingdom')}
    key, icon, title = map_data[st.session_state.stage]
    
    st.subheader(f"{icon} {title}")
    st.write(f"**Game Master:** {st.session_state.roles[key]['question']}")
    
    if ans := st.text_area("Your answer:"):
        if st.button("Next"):
            setattr(st.session_state, f"{key}_ans", ans)
            st.session_state.stage += 1
            st.rerun()

elif st.session_state.stage == 4:
    st.header("💎 Final Mindmap")
    prompt = f"Topic: {st.session_state.topic}. Synthesis (Micro: {st.session_state.micro_ans}, Meso: {st.session_state.meso_ans}, Macro: {st.session_state.macro_ans}). Create an IELTS Tree Diagram using arrows (->) for vocabulary."
    st.markdown(get_ai_response(prompt))
    if st.button("Restart"):
        st.session_state.clear()
        st.rerun()
