# VideoAnalysis.py
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os
import requests
import base64


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
    
    st.sidebar.image(f"data:image/png;base64,{encoded_logo}", use_column_width=True)
    st.sidebar.title("GemReel")
    st.sidebar.write("This application uses Gemini 1.5 Pro to answer your query about an uploaded video.")
    st.sidebar.write("## How to Use")
    st.sidebar.write("""
        - Enter a video URL (.mp4) or Upload a video file
        - Set the maximum word count for the summary.
        - Click the 'Analyze Video' button to see the result.
    """)

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_video_response(prompt, video_data):
    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
    response = model.generate_content([prompt, {"mime_type": "video/mp4", "data": video_data}])
    return response.text

def main():
    load_sidebar_content()
    st.header("GemReel")

    # User input for video file URL or file upload
    video_url = st.text_input("Enter a video URL (.mp4):")
    video_file = st.file_uploader("...or upload a video file (.mp4):", type=["mp4"])

    # Display and play the video file
    if video_url or video_file:
        if video_url:
            video_response = requests.get(video_url)
            video_bytes = video_response.content
            st.video(video_url)
        elif video_file:
            # To play video from an uploaded file
            st.video(video_file.getvalue(), format='video/mp4')

    # Query input from the user
    prompt = st.text_area("Enter your query about the video:")
    
    if st.button("Analyze Video"):
        if video_file:
            video_data = base64.b64encode(video_file.getvalue()).decode('utf-8')
        elif video_url:
            video_data = base64.b64encode(video_bytes).decode('utf-8')

        if video_data and prompt:
            analysis_result = get_video_response(prompt, video_data)
            st.subheader("Video Analysis Result")
            st.write(analysis_result)
        else:
            st.error("Please upload a video file or enter a URL and ensure a query is provided.")

if __name__ == "__main__":
    main()
