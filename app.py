import streamlit as st
import google.generativeai as genai

st.set_page_config(layout="centered")
st.title("🗡️ The Analytical Journey")

# 1. Sidebar nhập API Key
with st.sidebar:
    api_key = st.text_input("Enter Gemini API Key:", type="password")

if not api_key:
    st.info("👋 Game Master: Hello! Enter API Key in sidebar to begin.")
    st.stop()

genai.configure(api_key=api_key)

# 2. Quản lý trạng thái game
if 'stage' not in st.session_state:
    st.session_state.stage = 0

# 3. Logic trạm 0 (Bắt đầu)
if st.session_state.stage == 0:
    st.write("📖 Game Master: Tell me your story today!")
    topic = st.text_area("Topic:")
    
    if st.button("🚀 Begin Your Journey"):
        if topic:
            st.session_state.topic = topic
            st.session_state.stage = 1
            st.rerun() # Ép tải lại ngay lập tức
        else:
            st.warning("Please enter a topic!")

# 4. Logic các trạm RPG (được hiển thị khi stage > 0)
elif st.session_state.stage > 0:
    if 'roles' not in st.session_state:
        # Gọi AI lấy vai diễn ở đây
        model = genai.GenerativeModel('gemini-1.0-pro')
        prompt = f"Topic: '{st.session_state.topic}'. Give me 3 roles (Individual, Organization, Government) with 1 question each. Format: 'Role|Question' separated by ';;;'"
        response = model.generate_content(prompt)
        # Tách chuỗi đơn giản, không dùng JSON để tránh lỗi cú pháp
        parts = response.text.split(';;;')
        st.session_state.roles = [p.split('|') for p in parts if '|' in p]
    
    # Hiển thị trạm hiện tại
    s = st.session_state.stage - 1
    if s < len(st.session_state.roles):
        role_name, question = st.session_state.roles[s]
        st.subheader(f"Stage {st.session_state.stage}: {role_name}")
        st.write(f"**Game Master:** {question}")
        ans = st.text_area("Your thoughts:", key=f"ans_{s}")
        if st.button("Submit & Proceed"):
            st.session_state.stage += 1
            st.rerun()
    else:
        st.header("💎 The Treasure Board")
        st.write("Your quest is complete! Analysis complete.")
        if st.button("🔄 Restart"):
            st.session_state.clear()
            st.rerun()
