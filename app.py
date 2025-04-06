import streamlit as st
import pandas as pd
import google.generativeai as genai

# Page settings
st.set_page_config(page_title="📊 CSV Chatbot", layout="wide")

st.title("🤖 Interactive CSV Chatbot")
st.write("Upload a CSV, analyze data with a checkbox, and ask questions using AI!")

# --- 1. Gemini API Key ---
gemini_api_key = st.text_input(
    "🔐 Enter your Gemini API Key", 
    placeholder="Paste your Gemini API Key here...", 
    type="password"
)

# --- 2. Configure Gemini ---
model = None
if gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-pro")
        st.success("✅ Gemini API Key configured successfully!")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# --- 3. Initialize session states ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None

# --- 4. Upload CSV File ---
st.subheader("📁 Upload your CSV file")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.session_state.uploaded_data = df
        st.success("✅ File uploaded successfully!")
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"❌ Failed to load CSV: {e}")

# --- 5. Checkbox for triggering data analysis ---
st.subheader("📊 Control Data Analysis")

if st.checkbox("Click to analyze the uploaded data"):
    if st.session_state.uploaded_data is not None:
        df = st.session_state.uploaded_data
        st.write("### ℹ️ Basic Data Info:")
        st.write(df.info())
        st.write("### 📈 Summary Statistics:")
        st.dataframe(df.describe())
    else:
        st.warning("⚠️ No file uploaded yet.")

# --- 6. Chat Input with AI (Gemini) ---
st.subheader("💬 Ask questions about your data")

if model:
    user_prompt = st.chat_input("Type your question...")
    
    if user_prompt:
        # Show user message
        st.chat_message("user").markdown(user_prompt)
        st.session_state.chat_history.append(("user", user_prompt))

        # Create a data context
        context = ""
        if st.session_state.uploaded_data is not None:
            df = st.session_state.uploaded_data
            context += f"""
            Dataset Preview:
            {df.head(2).to_markdown()}
            
            Columns: {', '.join(df.columns)}
            """
        
        # Generate response from AI model
        try:
            response = model.generate_content(context + "\n\n" + user_prompt)
            bot_reply = response.text
        except Exception as e:
            bot_reply = f"❌ Gemini error: {e}"
        
        # Show assistant reply
        st.chat_message("assistant").markdown(bot_reply)
        st.session_state.chat_history.append(("assistant", bot_reply))
else:
    st.info("Please enter your Gemini API key above to start chatting.")
