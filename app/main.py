import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Streamlit page config (FAST)
st.set_page_config(
    page_title="Enterprise Customer Support",
    layout="centered"
)

st.title("Enterprise Customer Support")

# Lazy-load Gemini (CRITICAL FIX)
@st.cache_resource
def load_gemini():
    """
    Loads the Gemini model only once.
    Prevents Streamlit from hanging on startup.
    """
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    return genai.GenerativeModel("gemini-1.5-flash")  # fast model


# Cached response generation
@st.cache_data(show_spinner=False)
def generate_response(model, user_text: str) -> str:
    """
    Generates a Gemini response for the given input.
    Cached to improve performance.
    """
    prompt = f"""
You are an enterprise customer support assistant.

Guidelines:
- Respond professionally.
- Adapt to the user's message.
- Do NOT repeat generic or canned responses.
- Do NOT limit feedback categories.

Customer message:
\"\"\"{user_text}\"\"\"
"""
    response = model.generate_content(prompt)
    return response.text

# UI
user_input = st.text_area(
    "Enter your issue or feedback:",
    height=150
)

if st.button("Submit"):
    if not user_input.strip():
        st.warning("Please enter your message.")
    else:
        with st.spinner("Generating AI response..."):
            model = load_gemini()  # ✅ loaded ONLY when needed
            reply = generate_response(model, user_input)
            st.success(reply)
