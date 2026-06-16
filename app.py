import streamlit as st
import google.generativeai as genai
import json

# Lấy Key từ Két sắt (Secrets)
key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=key)

st.set_page_config(page_title="The Analytical Journey", layout="centered")

def get_ai_data(prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Tăng timeout để tránh tình trạng "load mãi không xong"
        response = model.generate_content(prompt, request_options={"timeout": 60})
        text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(text)
    except Exception as e:
        return None

st.title("🗡️ The Analytical Journey")

if 'stage' not in st.session_state: st.session_state.stage = 0

if st.session_state.stage == 0:
    st.info("👋 Game Master: Hello! Enter your topic:")
    if topic := st.text_area("Topic:"):
        if st.button("🚀 Start Adventure"):
            with st.spinner("Setting up the quest..."):
                roles = get_ai_data(f"Topic: '{topic}'. Create 3 RPG roles (Micro, Meso, Macro) with 1 question each. Return ONLY JSON: {{\"micro\": {{\"role\": \"\", \"question\": \"\"}}, \"meso\": {{\"role\": \"\", \"question\": \"\"}}, \"macro\": {{\"role\": \"\", \"question\": \"\"}}}}")
                if roles:
                    st.session_state.roles = roles
                    st.session_state.topic = topic
                    st.session_state.stage = 1
                    st.rerun()
                else: st.error("Quest failed. Please check your API Key!")
# (Các stage 1,2,3,4 giữ nguyên như cũ)
