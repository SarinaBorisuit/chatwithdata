import streamlit as st
import pandas as pd
import google.generativeai as genai

# Set up the Streamlit app layout
st.title("🤖 My Chatbot and Data Analysis App")
st.subheader("Conversation and Data Analysis")

# Capture Gemini API Key
gemini_api_key = st.text_input("Gemini API Key: ", placeholder="Type your API Key here...", type="password")

# Initialize the Gemini Model
model = None
if gemini_api_key:
    try:
        # Configure Gemini with the provided API Key
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-pro")
        st.success("Gemini API Key successfully configured.")
    except Exception as e:
        st.error(f"An error occurred while setting up the Gemini model: {e}")

# Initialize session state for storing chat history and data
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Initialize with an empty list
if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None  # Placeholder for uploaded CSV data

# Display previous chat history using st.chat_message (if available)
for role, message in st.session_state.chat_history:
    st.chat_message(role).markdown(message)

# Add a file uploader for CSV data
st.subheader("Upload CSV for Analysis")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
if uploaded_file is not None:
    try:
        # Load the uploaded CSV file
        st.session_state.uploaded_data = pd.read_csv(uploaded_file)
        st.success("File successfully uploaded and read.")
        st.dataframe(st.session_state.uploaded_data.head())
    except Exception as e:
        st.error(f"Failed to read the file: {e}")
