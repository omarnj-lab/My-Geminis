# CreateCustomApp.py
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os 
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
    st.sidebar.title("GemCustom")
    st.sidebar.write("This application will create a custom app based on your preferences")
    st.sidebar.write("## How to Use")
    st.sidebar.write("""
        - Select the type of your app.
        - Choose the AI model
        - Enter your custom prompt. 
        - Use the app.
    """)


load_dotenv()

# Load your API configuration and initialize the model
def load_model(model_name):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    return genai.GenerativeModel(model_name)

def generate_response(model, input_data, input_type, prompt):
    if input_type == "text":
        response = model.generate_content([prompt, {"text": input_data}])
    elif input_type == "image":
        encoded_image = base64.b64encode(input_data).decode('utf-8')
        response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": encoded_image}])
    elif input_type == "audio":
        encoded_audio = base64.b64encode(input_data).decode('utf-8')
        response = model.generate_content([prompt, {"mime_type": "audio/mpeg", "data": encoded_audio}])
    elif input_type == "video":
        encoded_video = base64.b64encode(input_data).decode('utf-8')
        response = model.generate_content([prompt, {"mime_type": "video/mp4", "data": encoded_video}])
    return response.text

def create_custom_app():
    load_sidebar_content()
    st.header("Create Your Own App")

    app_type = st.selectbox("Select the type of your app:", ["Text", "Image", "Audio", "Video"])
    model_choice = st.selectbox("Choose the AI model:", ['gemini-pro', 'gemini-pro-vision', 'gemini-1.5-pro-latest'])
    user_prompt = st.text_area("Enter your custom prompt:")

    model = load_model(model_choice)  # Load the selected model

    if app_type == "Text":
        user_query = st.text_area("Enter your text query:")
        if st.button("Generate Text"):
            response = generate_response(model, user_query, "text", user_prompt)
            st.write(f"Text Response: {response}")
    elif app_type == "Image":
        uploaded_image = st.file_uploader("Upload your image:", type=["jpg", "png", "jpeg"])
        if uploaded_image and st.button("Analyze Image"):
            response = generate_response(model, uploaded_image.getvalue(), "image", user_prompt)
            st.image(uploaded_image, caption="Uploaded Image")
            st.write(f"Image Analysis: {response}")
    elif app_type == "Audio":
        uploaded_audio = st.file_uploader("Upload your audio:", type=["mp3", "wav"])
        if uploaded_audio and st.button("Analyze Audio"):
            response = generate_response(model, uploaded_audio.getvalue(), "audio", user_prompt)
            st.audio(uploaded_audio)
            st.write(f"Audio Analysis: {response}")
    elif app_type == "Video":
        uploaded_video = st.file_uploader("Upload your video:", type=["mp4", "avi"])
        if uploaded_video and st.button("Analyze Video"):
            response = generate_response(model, uploaded_video.getvalue(), "video", user_prompt)
            st.video(uploaded_video)
            st.write(f"Video Analysis: {response}")

if __name__ == "__main__":
    create_custom_app()