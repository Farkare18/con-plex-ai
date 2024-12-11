# import streamlit as st
# import random
# import time
# import backend


# def response_generator(prompt):
#     response = backend.GenerateResponse(prompt)
#     for word in response.split():
#         yield word + " "
#         time.sleep(0.05)

# st.title("CON AI")

# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Accept user input
# if prompt := st.chat_input("What is up?"):
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     #display assistant response in chat message container
#     with st.chat_message("assistant"):
#         response = st.write_stream(response_generator(prompt))
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "assistant", "content": response})

#     # Add assistant message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     #display assistant response in chat message container
#     with st.chat_message("assistant"):
#         response = st.write_stream(response_generator(prompt))
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "assistant", "content": response})


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

def response_generator(prompt):
    response = backend.GenerateResponse(prompt)
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

# Function to play audio response
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function for voice input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            st.info("Processing...")
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."
        except sr.RequestError:
            return "Speech recognition service is unavailable."
        except sr.WaitTimeoutError:
            return "No input detected."

def listen():
    recognizer = sr.Recognizer()
    # Create placeholders for status messages
    listening_placeholder = st.empty()  # Placeholder for "Listening..."
    processing_placeholder = st.empty()  # Placeholder for "Processing..."
    
    try:
        with sr.Microphone() as source:
            listening_placeholder.info("Listening...")  # Display "Listening..."
            audio = recognizer.listen(source, timeout=None)
            listening_placeholder.empty()  # Clear "Listening..."
            
            processing_placeholder.info("Processing...")  # Display "Processing..."
            text = recognizer.recognize_google(audio)
            processing_placeholder.empty()  # Clear "Processing..."
            
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

st.title("CON-plex AI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Voice mode toggle
voice_mode = st.checkbox("Enable Voice Mode")

# Voice assistant chat interface
if voice_mode:
    prompt = st.text_input("Type or Speak your query:", key="chat-input")

    if st.button("Speak", key="voice-button"):
        voice_input = listen()
        if voice_input:
            prompt = voice_input

    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate response
        response = ''.join(response_generator(prompt))

        with st.chat_message("assistant"):
            st.markdown(response)
            # speak(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

# Accept user input from chat input box
if not voice_mode:
    if prompt := st.chat_input("ask me anything......"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate response
        response = ''.join(response_generator(prompt))

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response)

        # Add messages to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Play audio response
        speak(response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


