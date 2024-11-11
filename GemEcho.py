# AudioAnalysis.py
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os
import requests
import io
import base64
import tempfile


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    st.markdown(
        f'''
        <style>
        .stApp {{
            background-image: url(data:image/jpeg;base64,{encoded_string.decode()});
            background-size: 100%;
            height: auto!important;
        }}
        </style>
        ''',
        unsafe_allow_html=True
    )

add_bg_from_local('bg.png')

def load_sidebar_content():
    # Load your logo image
    logo_image = 'bgno.png'
    with open(logo_image, "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode('utf-8')
    
    st.sidebar.image(f"data:image/png;base64,{encoded_logo}", use_container_width=True)
    st.sidebar.title("GemEcho")
    st.sidebar.write("This application uses Gemini 1.5 Pro to answer your query about an uploaded audio")
    st.sidebar.write("## How to Use")
    st.sidebar.write("""
        - Enter a audio URL (.mp3) or Upload a audio file
        - you may hear its content after uploading it
        - Set the maximum word count for the summary.
        - Click the 'Analyze Audio' button to see the result.
    """)

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_audio_response(prompt, audio_data):
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    response = model.generate_content([prompt, {"mime_type": "audio/mpeg", "data": audio_data}])
    return response.text

def main():
    load_sidebar_content()
    st.header("GemEcho")

    audio_url = st.text_input("Enter an audio URL (.mp3):")
    audio_file = st.file_uploader("...or upload an audio file (.mp3):", type=["mp3"])

    if audio_url:
        st.audio(audio_url)

    if audio_file:
        # Create a temporary file to store the uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
            tmp.write(audio_file.getvalue())
            tmp_path = tmp.name
        
        # Play the audio using the temporary file
        st.audio(tmp_path)

    prompt = st.text_area("Enter your query about the audio:")
    
    if st.button("Analyze Audio"):
        if audio_file:
            with open(tmp_path, "rb") as f:
                audio_data = base64.b64encode(f.read()).decode('utf-8')
        elif audio_url:
            response = requests.get(audio_url)
            audio_data = base64.b64encode(response.content).decode('utf-8')

        if audio_data and prompt:
            analysis_result = get_audio_response(prompt, audio_data)
            st.subheader("Audio Analysis Result")
            st.write(analysis_result)
        else:
            st.error("Please upload an audio file or enter a URL and ensure a query is provided.")

if __name__ == "__main__":
    main()
