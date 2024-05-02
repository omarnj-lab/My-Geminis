# ImageDescription.py
from dotenv import load_dotenv
import streamlit as st
import os
import base64
from PIL import Image
import io
import google.generativeai as genai
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
    st.sidebar.title("GemPix")
    st.sidebar.write("This application uses Gemini 1.5 Pro with 1M Tokens Context Window to describe images and create stories based on uploaded image")
    st.sidebar.write("## How to Use")
    st.sidebar.write("""
        - Upload an image.
        - Enter your query about the image (like write a story about this image...)
        - Click the 'Describe Image' button to see the result.
    """)

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image_data):
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    encoded_image = base64.b64encode(image_data.getvalue()).decode('utf-8')
    response = model.generate_content([input_prompt, {"mime_type": "image/jpeg", "data": encoded_image}])
    return response.text

def main():
    load_sidebar_content()
    st.header("GemPix")

    uploaded_file = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"])
    user_query = st.text_area("Enter your query about the image:")

    if uploaded_file is not None:
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
        st.write("Image Uploaded Successfully")

    if st.button("Describe Image"):
        if uploaded_file and user_query:
            image_data = io.BytesIO(uploaded_file.getvalue())
            response = get_gemini_response(user_query, image_data)
            st.subheader("Image Description")
            st.write(response)
        else:
            st.error("Please upload an image and enter a query to describe it.")

if __name__ == "__main__":
    main()
