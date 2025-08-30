import streamlit as st
import cohere
from audio_output import speak_response,stop_speaking
from RealtimeSTT import AudioToTextRecorder
import time

# Set the title of the Streamlit app
st.title("Welcome to Cohere ChatBot application")

# Initialize Cohere client (Replace with your actual API key)
co = cohere.Client("pw8YsfdQvJ6MBLxGrsTEU9QXnoeEpzlUradVs70G")

# Initialize session state to store chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize loop flag
if "voice_loop" not in st.session_state:
    st.session_state.voice_loop = False

# Display previous messages in the chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def process_input(user_input):
    stop_speaking()  

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    history = [
        {
            "role": "User" if m["role"] == "user" else "Chatbot",
            "message": m["content"]
        }
        for m in st.session_state.messages
        if m["role"] in ["user", "assistant"]
    ]

    with st.chat_message("assistant"):
        response = co.chat_stream(
            model="command-r-plus",
            chat_history=history[:-1],
            message=user_input,
            citation_quality="fast"
        )

        placeholder = st.empty()
        full_response = ""

        for event in response:
            if hasattr(event, "event_type") and event.event_type == "text-generation":
                full_response += event.text
                placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
        speak_response(full_response)

def voice_loop():
    status = st.empty()
    recorder = AudioToTextRecorder()

    while st.session_state.voice_loop:
        status.markdown("Listening...")
        recorder.start()
        time.sleep(7)  # You can enhance this with real VAD later
        recorder.stop()

        voice_input = recorder.text().strip()
        status.empty()

        if voice_input:
            process_input(voice_input)
        else:
            st.warning("Didn't catch anything, listening again...")

# Create two columns: one for text input, one for voice button
col1, col2 = st.columns([8, 1])

with col1:
    prompt = st.chat_input("Say something...")

with col2:
    if st.button(" Start Voice Chat"):
        stop_speaking() 
        st.session_state.voice_loop = True
        voice_loop()
    if st.button("Stop"):
        st.session_state.voice_loop = False
        stop_speaking()
        st.success("Voice chat stopped.")

if prompt:
    process_input(prompt)
