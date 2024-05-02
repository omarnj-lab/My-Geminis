# Translation_app.py
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
    st.sidebar.title("GemLingo")
    st.sidebar.write("This application uses Gemini Pro to translate from one source langauge to another target language.")
    st.sidebar.write("## How to Use")
    st.sidebar.write("""
        - Enter Source Language.
        - Enter Target Language
        - Enter the sentence you want to translate.
        - Click the 'Translate' button to see the result.
    """)

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def translate_text(text, source_lang, target_lang):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Translate from {source_lang} to {target_lang}: {text}"
    response = model.generate_content(prompt)
    return response.text

def main():
    load_sidebar_content()
    st.header("GemLingo")
    source_lang = st.text_input("Source language:")
    target_lang = st.text_input("Target language:")
    text_to_translate = st.text_area("Enter text to translate:")
    if st.button("Translate"):
        translation = translate_text(text_to_translate, source_lang, target_lang)
        st.subheader("Translation")
        st.write(translation)

if __name__ == "__main__":
    main()
