import streamlit as st
import google.generativeai as genai
import json
import requests
from streamlit_lottie import st_lottie

# --- CẤU HÌNH API CỐ ĐỊNH ---
API_KEY = "AQ.Ab8RN6KRnYQ1CgzNOYdNu_gBdKkBVYxyUCPsCwNohJ8iOMLKTA" 
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="The Analytical Journey", page_icon="🗡️", layout="centered")

# --- HÀM TẢI ẢNH ĐỘNG (LOTTIE) ---
@st.cache_data
def load_lottie(url: str):
    try:
        r = requests.get(url, timeout=3)
        return r.json() if r.status_code == 200 else None
    except: return None

# Thư viện ảnh động cho từng trạm
anim_intro = load_lottie("https://lottie.host/80540450-48b4-4b11-a8ee-fdf4e9a1801c/S71N24QYpK.json")
anim_micro = load_lottie("https://lottie.host/d198115d-00eb-4043-9ddf-135e69e38f61/7Q9b9K2z5x.json") # Nhân vật đi bộ
anim_meso = load_lottie("https://lottie.host/57f12e12-4cf3-4ed1-b54f-12c8a1d0f5e1/LgT2zZ4O2n.json") # Tòa nhà hội quán
anim_macro = load_lottie("https://lottie.host/5b55de17-3843-42e6-a052-a5d625d3dfae/hBw1LCLrU0.json") # Lâu đài vĩ mô
anim_treasure = load_lottie("https://lottie.host/d73010b4-3a55-46eb-8e47-e14b1fec662e/Z1z2x3c4v5.json") # Rương kho báu

# --- KHỞI TẠO TIẾN TRÌNH ---
if 'stage' not in st.session_state:
    st.session_state.stage = 0
    st.session_state.topic = ""
    st.session_state.roles = {} 
    st.session_state.micro_ans = ""
    st.session_state.micro_fb = ""
    st.session_state.meso_ans = ""
    st.session_state.meso_fb = ""
    st.session_state.macro_ans = ""
    st.session_state.macro_fb = ""

def reset_game():
    for key in list(st.session_state.keys()): del st.session_state[key]
    st.rerun()

# --- HÀM GỌI AI THÔNG MINH ---
def get_dynamic_roles(topic):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    Topic: '{topic}'.
    Act as a Game Master. Analyze the topic and create 3 tailored RPG roles:
    1. Micro: An individual affected by this.
    2. Meso: An organizational leader involved.
    3. Macro: A top-tier societal/government figure.
    Generate a specific guiding question for each in English.
    Return ONLY a raw JSON object like this:
    {{"micro": {{"role": "Specific Name", "question": "..."}}, "meso": {{"role": "...", "question": "..."}}, "macro": {{"role": "...", "question": "..."}}}}
    """
    try:
        response = model.generate_content(prompt).text.replace('```json', '').replace('```', '').strip()
        return json.loads(response)
    except: return None

def get_ai_feedback(role, answer):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    The user (playing as {role}) answered: "{answer}". Note: They might use Vietnamese.
    1. Validate their point with a short English sentence.
    2. DO NOT write full sentences for their ideas. Suggest 3 high-level IELTS collocations/keywords related to their answer. 
    Format: "Great insight! Here are some powerful lexical resources: Word 1, Word 2, Word 3".
    """
    return model.generate_content(prompt).text

# --- GIAO DIỆN GAME ---
st.title("🗡️ The Analytical Journey")
st.markdown("*Level up your Critical Thinking with the Game Master*")
st.divider()

# TRẠM 0
if st.session_state.stage == 0:
    if anim_intro: st_lottie(anim_intro, height=200)
    st.info("📜 **[Game Master]:** Traveler, present the magic scroll (IELTS Topic) to begin. You can write your answers in Vietnamese or English later.")
    topic = st.text_area("Enter IELTS Writing Task 2 Topic:")
    if st.button("🚀 Begin the Journey"):
        if topic:
            with st.spinner("Game Master is reading the stars to assign your destiny..."):
                roles = get_dynamic_roles(topic)
                if roles:
                    st.session_state.roles = roles
                    st.session_state.topic = topic
                    st.session_state.stage = 1
                    st.rerun()
                else: st.error("The magic failed. Please try again!")
        else: st.warning("Please enter a topic!")

# TRẠM 1: MICRO
elif st.session_state.stage == 1:
    if anim_micro: st_lottie(anim_micro, height=150)
    st.subheader("🏕️ Stage 1: The Micro Village")
    role = st.session_state.roles.get('micro', {}).get('role', 'Villager')
    question = st.session_state.roles.get('micro', {}).get('question', '')
    
    st.success(f"**[Game Master]:** You have possessed the body of a **{role}**.\n\n*\"{question}\"*")
    ans = st.text_area("Answer (Tiếng Anh hoặc Tiếng Việt đều được):", height=100)
    
    if st.button("Submit Insight ➡️"):
        if ans:
            with st.spinner("Gathering Micro insights..."):
                st.session_state.micro_ans = ans
                st.session_state.micro_fb = get_ai_feedback(role, ans)
                st.session_state.stage = 1.5
                st.rerun()

elif st.session_state.stage == 1.5:
    st.info(f"**[Game Master]:** {st.session_state.micro_fb}")
    if st.button("Travel to The Meso Guild 🗺️"):
        st.session_state.stage = 2
        st.rerun()

# TRẠM 2: MESO
elif st.session_state.stage == 2:
    if anim_meso: st_lottie(anim_meso, height=150)
    st.subheader("🏛️ Stage 2: The Meso Guild")
    role = st.session_state.roles.get('meso', {}).get('role', 'Guild Master')
    question = st.session_state.roles.get('meso', {}).get('question', '')
    
    st.success(f"**[Game Master]:** You leveled up to a **{role}**.\n\n*\"{question}\"*")
    ans = st.text_area("Answer:", height=100)
    
    if st.button("Submit Strategy ➡️"):
        if ans:
            with st.spinner("Analyzing organizational strategy..."):
                st.session_state.meso_ans = ans
                st.session_state.meso_fb = get_ai_feedback(role, ans)
                st.session_state.stage = 2.5
                st.rerun()

elif st.session_state.stage == 2.5:
    st.info(f"**[Game Master]:** {st.session_state.meso_fb}")
    if st.button("Enter The Macro Kingdom 🗺️"):
        st.session_state.stage = 3
        st.rerun()

# TRẠM 3: MACRO
elif st.session_state.stage == 3:
    if anim_macro: st_lottie(anim_macro, height=150)
    st.subheader("🏰 Stage 3: The Macro Kingdom")
    role = st.session_state.roles.get('macro', {}).get('role', 'King')
    question = st.session_state.roles.get('macro', {}).get('question', '')
    
    st.success(f"**[Game Master]:** Welcome to the throne, **{role}**.\n\n*\"{question}\"*")
    ans = st.text_area("Answer:", height=100)
    
    if st.button("Declare Policy ➡️"):
        if ans:
            with st.spinner("Pondering global impact..."):
                st.session_state.macro_ans = ans
                st.session_state.macro_fb = get_ai_feedback(role, ans)
                st.session_state.stage = 3.5
                st.rerun()

elif st.session_state.stage == 3.5:
    st.info(f"**[Game Master]:** {st.session_state.macro_fb}")
    if st.button("Unlock The Treasure Board 💎"):
        st.session_state.stage = 4
        st.rerun()

# ĐÍCH ĐẾN: MINDMAP
elif st.session_state.stage == 4:
    st.balloons()
    if anim_treasure: st_lottie(anim_treasure, height=200)
    st.header("💎 The Treasure Board")
    
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    Topic: {st.session_state.topic}
    Student's raw ideas: 
    Micro: {st.session_state.micro_ans}
    Meso: {st.session_state.meso_ans}
    Macro: {st.session_state.macro_ans}
    
    MANDATORY RULES:
    1. DO NOT write full sentences or paragraphs.
    2. Synthesize their ideas using the "Staircase" framework (Micro, Meso, Macro) and the "Cascading Why" framework (Core -> Why -> So What).
    3. Use ONLY keywords and short noun/verb phrases connected by arrows ('->').
    4. Language: English.
    
    Example output format:
    ### 🏕️ Micro Level
    * Core issue -> Immediate feeling -> Final consequence
    
    ### 🏛️ Meso Level
    * Action -> Operational challenge -> Result
    """
    
    with st.spinner('Forging the Mindmap Diagram...'):
        st.markdown(model.generate_content(prompt).text)

    st.divider()
    if st.button("🔄 Start New Journey"): reset_game()
