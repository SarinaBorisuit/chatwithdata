import streamlit as st
import pandas as pd
import google.generativeai as genai

# Set up the Streamlit app layout
st.set_page_config(page_title="Chatbot & Data App", layout="wide")
st.title("🤖 My Chatbot and Data Analysis App")
st.subheader("Conversation and Data Analysis")

# Capture Gemini API Key
gemini_api_key = st.text_input(
    "🔐 Gemini API Key:", 
    placeholder="Type your API Key here...", 
    type="password"
)

# Initialize the Gemini Model
model = None
if gemini_api_key:
    try:
        # Configure Gemini with the provided API Key
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-pro")
        st.success("✅ Gemini API Key successfully configured.")
    except Exception as e:
        st.error(f"❌ An error occurred while setting up the Gemini model: {e}")

# Initialize session state for storing chat history and data
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Chat history list

if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None  # CSV file placeholder

# Display previous chat history
for role, message in st.session_state.chat_history:
    st.chat_message(role).markdown(message)

# File uploader
st.subheader("📁 Upload CSV for Analysis")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Load the uploaded CSV file
        st.session_state.uploaded_data = pd.read_csv(uploaded_file)
        st.success("✅ File successfully uploaded and read.")
        st.dataframe(st.session_state.uploaded_data.head())
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")

# Checkbox to trigger data analysis
if st.session_state.uploaded_data is not None:
    if st.checkbox("🔍 Analyze the uploaded data"):
        df = st.session_state.uploaded_data
        st.write("### Data Summary:")
        st.dataframe(df.describe())
        st.write("### Columns:", list(df.columns))

# Chat section
if model:
    user_prompt = st.chat_input("💬 Ask me something about your data or anything...")

    if user_prompt:
        # Display user message
        st.chat_message("user").markdown(user_prompt)
        st.session_state.chat_history.append(("user", user_prompt))

        # Provide context if data is uploaded
        context = ""
        if st.session_state.uploaded_data is not None:
            df = st.session_state.uploaded_data
            context = f"""
            Data preview:
            {df.head(2).to_markdown()}
            Columns: {', '.join(df.columns)}
            """

        # Generate AI response
        try:
            response = model.generate_content(context + "\n\n" + user_prompt)
            reply = response.text
        except Exception as e:
            reply = f"❌ Gemini error: {e}"

        st.chat_message("assistant").markdown(reply)
        st.session_state.chat_history.append(("assistant", reply))
else:
    st.info("🔑 Please enter your Gemini API key to activate the chatbot.")
