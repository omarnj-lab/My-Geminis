# Summarization_app.py
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import base64
import sys

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
    st.sidebar.title("Geminize")
    st.sidebar.write("This application uses Gemini-Pro to summarize text into a concise form.")
    st.sidebar.write("## How to Use")
    st.sidebar.write("""
        - Enter the text you want to summarize in the text area.
        - Set the maximum word count for the summary.
        - Click the 'Summarize' button to see the result.
    """)


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def summarize_text(text, max_words):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Summarize the following text to {max_words} words: {text}"
    response = model.generate_content(prompt)
    return response.text

def main():
    load_sidebar_content()

    st.header("Geminize")
    user_input = st.text_area("Enter text to summarize:")
    word_count = st.number_input("Enter max word count for summary:", min_value=10)
    if st.button("Summarize"):
        summary = summarize_text(user_input, word_count)
        st.subheader("Summary")
        st.write(summary)

if __name__ == "__main__":
    main()
