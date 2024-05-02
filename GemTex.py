# TextAnalysis.py
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
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
    st.sidebar.title("GemTex")
    st.sidebar.write("This application uses Gemini 1.5 Pro to generate text based on your Query.")
    st.sidebar.write("It is very advanced since its context length is 1M Token.")
    st.sidebar.write("## How to Use")
    st.sidebar.write("""
        - Enter What you needs to be generated as text (Email,Letter,Story, etc..).
        - Click the 'Generate Text' button to see the result.
    """)

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_text(query):
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content(query)
    return response.text

def main():
    load_sidebar_content()
    st.header("GemTex")

    query = st.text_area("Enter your query:", height=100)
    
    if st.button("Generate Text"):
        if query:
            generated_text = generate_text(query)
            st.subheader("Generated Text")
            st.write(generated_text)
        else:
            st.error("Please enter a query to generate text.")

if __name__ == "__main__":
    main()
