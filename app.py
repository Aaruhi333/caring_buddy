import streamlit as st

import cohere

import os

from dotenv import load_dotenv
 
# Load environment variables

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
 
# Initialize Cohere client

co = cohere.Client(COHERE_API_KEY)
 
def get_ai_response(user_input):

    response = co.generate(

        model='command',

        prompt=user_input,

        max_tokens=100

    )

    return response.generations[0].text.strip()
 
# Streamlit UI

st.set_page_config(page_title="Caring Buddy - Healthcare Chatbot", page_icon="💙")

st.title("💙 Caring Buddy - Your Healthcare Companion")

st.write("👩‍⚕️ How can I assist you with your health today?")
 
# Chat input

user_input = st.text_input("💬 Ask a health-related question:", "")

if st.button("Send 🏥") and user_input:

    response = get_ai_response(user_input)

    st.markdown(f"**🤖 Caring Buddy:** {response}")
 
# Sidebar for additional information

st.sidebar.header("🩺 About Caring Buddy")

st.sidebar.write("Caring Buddy is an AI-powered healthcare chatbot designed to provide general health guidance. Always consult a professional for medical advice.")

 
