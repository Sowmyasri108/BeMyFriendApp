import streamlit as st
import openai
from gtts import gTTS
import os
import datetime

# --- CONFIGURATION ---
openai.api_key = st.secrets["openai_key"]
st.set_page_config(page_title="BeMyFriend 🌈", page_icon="🫂", layout="centered")

# --- STYLE THEMES ---
themes = {
    "Cute": {"bg": "#fff0f6", "text": "#4a4a4a", "title": "#ff69b4", "font": "Comic Sans MS"},
    "Professional": {"bg": "#ffffff", "text": "#111", "title": "#111", "font": "Arial"},
    "Dark": {"bg": "#1e1e1e", "text": "#f1f1f1", "title": "#f78c6b", "font": "Verdana"},
    "Calm": {"bg": "#f0fff4", "text": "#305050", "title": "#6b705c", "font": "Georgia"},
}

# --- USER PREFERENCES ---
st.sidebar.title("🎨 Personalization")
theme_choice = st.sidebar.selectbox("Choose Theme", list(themes.keys()))
tone = st.sidebar.selectbox("🧠 AI Tone", ["Healing", "Poetic", "Funny", "Formal"])
gender = st.sidebar.radio("🧑 Choose AI Personality", ["Girl", "Boy"])
brain_mode = st.sidebar.selectbox("🧠 Brain Mode", ["None", "Mentor (Coding)", "Explorer (World)", "Quiz"])

# --- APPLY THEME ---
theme = themes[theme_choice]
st.markdown(f"""
    <style>
    body {{ background-color: {theme['bg']}; color: {theme['text']}; font-family: {theme['font']}; }}
    .stApp h1, h2, h3 {{ color: {theme['title']}; text-align: center; }}
    </style>
""", unsafe_allow_html=True)

# --- LOGO + AVATAR ---
st.image("https://i.imgur.com/YGH8fJn.png", width=100)  # Your custom logo here
if gender == "Girl":
    st.image("https://i.imgur.com/WoY9h0U.png", width=100)
else:
    st.image("https://i.imgur.com/rdm3W9t.png", width=100)

# --- HEADER ---
st.markdown(f"<h1>💛 BeMyFriend – Your Emotional AI Companion</h1>", unsafe_allow_html=True)

# --- INPUTS ---
mood = st.text_input("💭 What's your current mood?", placeholder="Happy, anxious, excited...")
prompt = st.text_input("🗣 Tell your AI friend something or ask anything", placeholder="I'm feeling lonely today...")

# --- GPT PERSONALITY ---
def get_prompt_context():
    system_prompt = f"You are a {tone.lower()} and emotionally intelligent AI companion."
    if brain_mode == "Mentor (Coding)":
        system_prompt = "You are a programming tutor. Help with Python, Java, or DSA topics."
    elif brain_mode == "Explorer (World)":
        system_prompt = "You are a global explorer AI. Share facts about history, science, space, geography."
    elif brain_mode == "Quiz":
        system_prompt = "You are a friendly quiz master. Ask me quiz questions in random topics."
    return system_prompt

# --- CHAT FUNCTION ---
def chat_with_ai(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": get_prompt_context()},
            {"role": "user", "content": user_input}
        ]
    )
    return response['choices'][0]['message']['content']

# --- TTS FUNCTION ---
def speak_text(text):
    try:
        tts = gTTS(text)
        tts.save("response.mp3")
        audio_file = open("response.mp3", "rb")
        st.audio(audio_file.read(), format="audio/mp3")
        audio_file.close()
        os.remove("response.mp3")
    except:
        st.error("Voice output failed. Try again later.")

# --- AI RESPONSE ---
if prompt:
    st.markdown("💬 *You:* " + prompt)
    with st.spinner("Your friend is thinking..."):
        reply = chat_with_ai(prompt)
        st.markdown("🧠 *BeMyFriend:* " + reply)
        speak_text(reply)

# --- SAFE SPACE MODE ---
st.markdown("## 🧘 Safe Space Mode")
if st.button("Enter Safe Space"):
    st.balloons()
    st.success("🌿 You're safe. Take a deep breath...")
    st.audio("https://cdn.pixabay.com/download/audio/2022/03/15/audio_7cc68d2d6b.mp3", format="audio/mp3")
    st.markdown("### 🌬 Breathing Guide:\n- Inhale 4… Hold 4… Exhale 4… Repeat 3x")

# --- JOURNAL WITH PIN ---
st.markdown("## 📔 Journal – Secret Diary")
with st.expander("🔐 Unlock with 4-digit PIN"):
    pin = st.text_input("Enter PIN", type="password")
    if pin == "1234":  # You can change this
        st.success("Unlocked!")
        journal_text = st.text_area("✍ Today's Thoughts", placeholder="What do you want to remember today?")
        if st.button("💾 Save Entry"):
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            with open("journal.txt", "a", encoding="utf-8") as f:
                f.write(f"\n---\n🕒 {now}\nMood: {mood}\nPrompt: {prompt}\nJournal: {journal_text}\n")
            st.success("✨ Saved to your diary.")
    elif pin:
        st.error("Incorrect PIN ❌")

# --- FOOTER ---
st.markdown("---")
st.caption("Made with 💛 using GPT-4, Streamlit, and your imagination.")