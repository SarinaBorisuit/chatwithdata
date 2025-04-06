import streamlit as st
import pandas as pd
import google.generativeai as genai

# Page settings
st.set_page_config(page_title="CSV Chatbot", layout="wide")

st.title("📊 CSV File Uploader with Chatbot")
st.subheader("Upload your CSV and explore it with a chatbot assistant")

# --- Gemini API Key Input ---
gemini_api_key = st.text_input(
    "🔐 Enter your Gemini API Key", 
    placeholder="Paste your API Key here...", 
    type="password"
)

model = None
if gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-pro")
        st.success("✅ Gemini API Key configured!")
    except Exception as e:
        st.error(f"❌ Failed to configure Gemini: {e}")

# --- Session States ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None

# --- CSV Upload ---
st.subheader("📁 Upload a CSV File")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.session_state.uploaded_data = df
        st.success("✅ File uploaded successfully!")
        
        st.write("### 🔍 Data Preview:")
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"❌ Could not read the CSV: {e}")

# --- Chat Interface ---
st.subheader("💬 Chat About Your Data")

if model:
    user_prompt = st.chat_input("Ask about your data or anything else...")
    
    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        st.session_state.chat_history.append(("user", user_prompt))
        
        # Add DataFrame info to the context if available
        context = ""
        if st.session_state.uploaded_data is not None:
            context = f"""
            Here's the preview of the uploaded CSV:
            {st.session_state.uploaded_data.head(2).to_markdown()}
            Columns: {', '.join(st.session_state.uploaded_data.columns)}
            """

        try:
            response = model.generate_content(context + "\n\n" + user_prompt)
            bot_reply = response.text
        except Exception as e:
            bot_reply = f"❌ Gemini error: {e}"
        
        st.chat_message("assistant").markdown(bot_reply)
        st.session_state.chat_history.append(("assistant", bot_reply))
else:
    st.info("👆 Please enter your Gemini API key to activate the chatbot.")

