import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Check API key
if not api_key:
    st.error("❌ Error: GEMINI_API_KEY not found in .env file.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

# Streamlit config
st.set_page_config(
    page_title="Cultural Emotion Translator 🌍",
    page_icon="💫",
    layout="centered"
)

# --- Custom Styles ---
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f5f7fa;
    }
    .stTextInput > div > div > input {
        padding: 10px;
        border-radius: 8px;
        font-size: 16px;
    }
    .stSelectbox > div {
        border-radius: 8px;
    }
    .stButton button {
        background-color: #2c3e50;
        color: #fff;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        font-size: 16px;
    }
    .stButton button:hover {
        background-color: #34495e;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color:#2c3e50;'>🌍 Cultural Emotion Translator</h1>
        <p style='font-size:16px; color:#555;'>Transform feelings into poetry, letters, or quotes — across cultures & languages</p>
    </div>
""", unsafe_allow_html=True)
st.markdown("---")

# --- Inputs ---
st.subheader("💬 Describe Your Emotion")

emotion = st.text_input("Emotion (e.g. Love, Loneliness, Gratitude):")
language = st.selectbox("🌐 Target Language", ["English", "Urdu", "Arabic", "French", "Spanish", "Turkish", "German"])
style = st.selectbox("🎨 Output Style", ["Poem", "Short Letter", "Quote", "Monologue"])

# --- Generate ---
if st.button("✨ Generate Expression"):
    if not emotion.strip():
        st.warning("⚠️ Please enter an emotion.")
    else:
        with st.spinner("Generating your cultural expression..."):
            prompt = f"""
            Write a refined, culturally aware {style} in {language} based on the emotion "{emotion}".
            The response should be short, meaningful, and emotionally rich. No explanation — only the creative result.
            """
            try:
                response = model.generate_content(prompt)
                result = response.text.strip()

                if not result:
                    st.error("⚠️ Empty response from Gemini.")
                else:
                    st.success("✅ Expression generated successfully!")
                    st.text_area(f"📜 Your {style} in {language}:", result, height=200)
                    st.download_button("⬇️ Download", result, f"{emotion}_{language}_{style}.txt", "text/plain")

            except Exception as e:
                st.error(f"❌ Gemini Error:\n{e}")

# --- Footer ---
st.markdown("---")
st.markdown("""
    <div style='text-align:center; font-size:13px; color:gray;'>
        Developed by <strong>Khanzadi</strong> • Powered by Google Gemini
    </div>
""", unsafe_allow_html=True)
