import streamlit as st

st.set_page_config(page_title="🎧 Listening Practice", layout="wide")
st.title("🎧 Listening Practice Tool")

audio_file = st.file_uploader("Upload your audio file (MP3/WAV)", type=["mp3", "wav"])

if audio_file:
    audio_bytes = audio_file.read()
    filetype = audio_file.type
    st.audio(audio_bytes, format=filetype)
    st.success("✅ Audio loaded. Use the native controls to play and pause.")
