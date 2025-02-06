import cohere
import streamlit as st
import os
from gtts import gTTS
import speech_recognition as sr
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
COHERE_API_KEY = os.getenv("6Xlg2kt7Hj40n5HvRvZt2DrQrDmvUp0SDdaVGQwc")

# Initialize Cohere client
co = cohere.Client(COHERE_API_KEY)

# Language options
language_options = {
    "English": "en",
    "Tamil (தமிழ்)": "ta",
    "Hindi (हिन्दी)": "hi",
    "Malayalam (മലയാളം)": "ml",
    "Telugu (తెలుగు)": "te",
    "Marathi (मराठी)": "mr"
}

def get_ai_response(user_input, target_language):
    """Generates AI response using Cohere and translates it."""
    prompt = f"You are a professional healthcare chatbot. Answer this medical question as clearly, accurately, and professionally as possible:\n\n{user_input}\n\nProvide a complete, informative response."

    # Increase the max_tokens limit to allow longer responses
    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=300,  # Increased token limit
        temperature=0.7
    ).generations[0].text.strip()

    # Translate response if needed
    if target_language != "en":
        response = GoogleTranslator(source="auto", target=target_language).translate(response)

    return response

def voice_to_text():
    """Converts speech to text and listens continuously."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Speak now...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand your speech."
        except sr.RequestError:
            return "Speech recognition service is not available."

def text_to_speech(text, language):
    """Converts text to speech using gTTS and plays it in Streamlit."""
    if language != "en":
        text = GoogleTranslator(source="auto", target="en").translate(text)  # Convert to English for speech

    tts = gTTS(text=text, lang='en')  # Set language to English for better speech output
    
    # Specify a folder to store the audio temporarily
    audio_folder = "audio_files"
    os.makedirs(audio_folder, exist_ok=True)  # Create folder if not exists
    
    # Create a unique filename for the MP3 file
    temp_audio_path = os.path.join(audio_folder, "output_audio.mp3")
    
    # Save the speech to the file
    tts.save(temp_audio_path)
    
    # Play the saved audio file using Streamlit
    st.audio(temp_audio_path, format="audio/mp3")

# Streamlit UI
st.set_page_config(page_title="Caring Buddy - Healthcare Chatbot", page_icon="💙")
st.title("💙 Caring Buddy - Your Healthcare Companion")
st.write("👩‍⚕️ How can I assist you with your health today?")

# Language selection dropdown
selected_language = st.selectbox("🌍 Choose Language:", list(language_options.keys()))
target_language = language_options[selected_language]

# Voice-to-text button
if st.button("🎙️ Speak"):
    user_input = voice_to_text()
    st.text(f"🗣️ You said: {user_input}")
    
    # Translate input to English if needed
    if target_language != "en":
        user_input = GoogleTranslator(source="auto", target="en").translate(user_input)

    # Get AI response
    response = get_ai_response(user_input, target_language)

    # Show response and generate image from AI (if any functionality added for image)
    st.markdown(f"**🤖 Caring Buddy:** {response}")

    # Convert AI response to speech
    text_to_speech(response, target_language)

# Sidebar for additional information
st.sidebar.header("🩺 About Caring Buddy")
st.sidebar.write("Caring Buddy is an AI-powered healthcare chatbot designed to provide general health guidance. Always consult a professional for medical advice.")


