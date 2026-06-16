import streamlit as st
import google.generativeai as genai
import json
import requests

st.set_page_config(page_title="The Analytical Journey", layout="centered")

# --- SIDEBAR: Cấu hình ---
with st.sidebar:
    st.header("🔑 Cấu hình kết nối")
    user_api_key = st.text_input("Dán Gemini API Key (Free Tier):", type="password")

if not user_api_key:
    st.title("🗡️ The Analytical Journey")
    st.info("👋 **Game Master:** Chào lữ khách! Hãy dán 'Chìa khóa ma thuật' (API Key) ở cột bên trái để bắt đầu.")
    st.stop()

genai.configure(api_key=user_api_key)

# --- HÀM XỬ LÝ AI ---
def get_ai_response(prompt, is_json=False):
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        response = model.generate_content(prompt)
        text = response.text
        # Loại bỏ markdown code blocks một cách an toàn
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text) if is_json else text
    except Exception as e:
        return None

# --- KHỞI TẠO TIẾN TRÌNH ---
if 'stage' not in st.session_state:
    st.session_state.stage = 0

st.title("🗡️ The Analytical Journey")

# TRẠM 0
if st.session_state.stage == 0:
    st.info("👋 **Game Master:** Chào bạn! Hãy nhập đề bài IELTS Writing Task 2 để bắt đầu.")
    if topic := st.text_area("Nhập đề bài tại đây:"):
        if st.button("🚀 Bắt đầu hành trình"):
            with st.spinner("Game Master đang chuẩn bị bối cảnh..."):
                prompt = f"Topic: '{topic}'. Create 3 RPG roles (Micro, Meso, Macro) with 1 question each. Return ONLY JSON: {{\"micro\": {{\"role\": \"\", \"question\": \"\"}}, \"meso\": {{\"role\": \"\", \"question\": \"\"}}, \"macro\": {{\"role\": \"\", \"question\": \"\"}}}}"
                roles = get_ai_response(prompt, True)
                if roles:
                    st.session_state.roles = roles
                    st.session_state.topic = topic
                    st.session_state.stage = 1
                    st.rerun()
                else: st.error("Lỗi AI: Vui lòng kiểm tra lại Key hoặc chủ đề.")

# CÁC TRẠM 1-3
elif st.session_state.stage <= 3:
    map_data = {1: ('micro', '🏕️', 'Micro Village'), 2: ('meso', '🏛️', 'Meso Guild'), 3: ('macro', '🏰', 'Macro Kingdom')}
    key, icon, title = map_data[st.session_state.stage]
    
    st.subheader(f"{icon} {title}")
    st.write(f"**{st.session_state.roles[key]['role']}:** {st.session_state.roles[key]['question']}")
    
    if ans := st.text_area("Câu trả lời của bạn:", key=f"ans_{key}"):
        if st.button("Gửi insight ➡️"):
            setattr(st.session_state, f"{key}_ans", ans)
            st.session_state.stage += 1
            st.rerun()

# TRẠM 4
elif st.session_state.stage == 4:
    st.balloons()
    st.header("💎 The Treasure Board")
    prompt = f"Topic: {st.session_state.topic}. Ideas: Micro:{st.session_state.micro_ans}, Meso:{st.session_state.meso_ans}, Macro:{st.session_state.macro_ans}. Create a Tree Diagram (use arrow ->) for an IELTS outline."
    st.markdown(get_ai_response(prompt))
    if st.button("🔄 Chơi lại từ đầu"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
