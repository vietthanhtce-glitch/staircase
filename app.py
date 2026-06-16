import streamlit as st
import google.generativeai as genai
import json

# --- CONFIG ---
API_KEY = "DÁN_API_KEY_CỦA_BẠN_VÀO_ĐÂY"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="The Analytical Journey", layout="centered")

# --- HÀM AI GIAO TIẾP ---
def get_ai_data(prompt, is_json=False):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(text) if is_json else text
    except Exception as e:
        st.error(f"System Error: {e}")
        return None

# --- GIAO DIỆN CHÍNH ---
st.title("🗡️ The Analytical Journey")
st.markdown("*IELTS Writing Task 2 Brainstorming RPG*")

if 'stage' not in st.session_state:
    st.session_state.stage = 0

# TRẠM 0
if st.session_state.stage == 0:
    st.info("👋 **Game Master:** Hello! I am your mentor. Please enter an IELTS Writing Task 2 topic to start our quest.")
    if topic := st.text_area("Enter your topic here:"):
        if st.button("🚀 Start Adventure"):
            with st.spinner("Setting up the quest..."):
                prompt = f"Topic: '{topic}'. Act as a friendly mentor. Assign 3 roles (Micro, Meso, Macro) with 1 guiding question in English for each. Return ONLY JSON: {{\"micro\": {{\"role\": \"\", \"question\": \"\"}}, \"meso\": {{\"role\": \"\", \"question\": \"\"}}, \"macro\": {{\"role\": \"\", \"question\": \"\"}}}}"
                roles = get_ai_data(prompt, True)
                if roles:
                    st.session_state.roles = roles
                    st.session_state.topic = topic
                    st.session_state.stage = 1
                    st.rerun()

# CÁC TRẠM (1, 2, 3)
elif st.session_state.stage <= 3:
    map_data = {1: ('micro', '🏕️', 'Micro Village'), 2: ('meso', '🏛️', 'Meso Guild'), 3: ('macro', '🏰', 'Macro Kingdom')}
    key, icon, title = map_data[st.session_state.stage]
    
    st.subheader(f"{icon} {title}")
    st.write(f"**Game Master:** As {st.session_state.roles[key]['role']}, {st.session_state.roles[key]['question']}")
    
    if ans := st.text_area("Your thoughts (or answer):", key=f"ans_{key}"):
        if st.button("Submit & Continue ➡️"):
            setattr(st.session_state, f"{key}_ans", ans)
            st.session_state.stage += 1
            st.rerun()

# TRẠM 4
elif st.session_state.stage == 4:
    st.balloons()
    st.header("💎 The Treasure Board")
    st.write("Here is your logical mindmap for the essay:")
    
    prompt = f"Topic: {st.session_state.topic}. Ideas: Micro:{st.session_state.micro_ans}, Meso:{st.session_state.meso_ans}, Macro:{st.session_state.macro_ans}. Create a logical Tree Diagram (use ->) of English keywords and vocabulary."
    st.markdown(get_ai_data(prompt))
    
    if st.button("🔄 Restart Quest"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
