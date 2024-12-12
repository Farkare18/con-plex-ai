import streamlit as st
import random
import time
import backend
import pyttsx3  # For TTS
import speech_recognition as sr  # For STT

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speech rate
engine.setProperty('voice', engine.getProperty('voices')[0].id)  # Choose a voice

# Sidebar
st.sidebar.title("Settings")
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []

assistant_personality = st.sidebar.selectbox(
    "Assistant Personality",
    options=["Friendly", "Professional", "Witty", "Casual"],
    index=0
)
response_speed = st.sidebar.slider("Response Speed (seconds per word):", 0.01, 0.5, 0.05, 0.01)
st.sidebar.markdown("### About")
st.sidebar.info(
    "CON-plex AI is a conversational assistant built with Streamlit. "
    "It supports text and voice interaction and adapts to your preferred personality style."
)

# Function to generate responses
def response_generator(prompt):
    personality_map = {
        "Friendly": "I am here to help in the most cheerful way!",
        "Professional": "I aim to maintain a professional tone in all interactions.",
        "Witty": "Let me spice up the answers with some humor!",
        "Casual": "Let's keep it chill and relaxed."
    }
    personality_intro = personality_map.get(assistant_personality, "")
    response = personality_intro + " " + backend.GenerateResponse(prompt)
    for word in response.split():
        yield word + " "
        time.sleep(response_speed)

# Function to play audio response
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function for voice input
def listen():
    recognizer = sr.Recognizer()
    listening_placeholder = st.empty()  # Placeholder for "Listening..."
    processing_placeholder = st.empty()  # Placeholder for "Processing..."
    
    try:
        with sr.Microphone() as source:
            listening_placeholder.info("Listening...")
            audio = recognizer.listen(source, timeout=None)
            listening_placeholder.empty()
            processing_placeholder.info("Processing...")
            text = recognizer.recognize_google(audio)
            processing_placeholder.empty()
            return text
    except sr.UnknownValueError:
        listening_placeholder.empty()
        processing_placeholder.empty()
        return "Sorry, I didn't catch that."
    except sr.RequestError:
        listening_placeholder.empty()
        processing_placeholder.empty()
        return "Speech recognition service is unavailable."
    except sr.WaitTimeoutError:
        listening_placeholder.empty()
        processing_placeholder.empty()
        return "No input detected."
    except Exception as e:
        listening_placeholder.empty()
        processing_placeholder.empty()
        return f"An error occurred: {e}"

# Main app
st.title("CON-plex AI: Your Conversational Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat interface
voice_mode_toggle = st.checkbox("Enable Voice Mode", key="voice_mode")
prompt = st.chat_input("Type your message here...")

if voice_mode_toggle and st.button("Speak", key="voice_button"):
    voice_input = listen()
    if voice_input:
        prompt = voice_input

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response
    response = ''.join(response_generator(prompt))

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)

    # Play audio response if voice mode is enabled
    if voice_mode_toggle:
        speak(response)

    # Add response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
