# QA_app.py
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
    
    st.sidebar.image(f"data:image/png;base64,{encoded_logo}", use_container_width=True)
    st.sidebar.title("GemQuest")
    st.sidebar.write("This application uses Gemini Pro to answer questions based on category and user query")
    st.sidebar.write("## How to Use")
    st.sidebar.write("""
        - Choose category from Drop List
        - Enter your question 
        - Click the 'Answer' button to see the result.
    """)

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_answer(question, category):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Question: {question}\nCategory: {category}\nAnswer:"
    response = model.generate_content(prompt)
    return response.text

def main():
    load_sidebar_content()
    st.header("GemQuest")
    category = st.text_input("Enter category:")
    question = st.text_input("Ask a question:")
    if st.button("Get Answer"):
        answer = get_answer(question, category)
        st.subheader("Answer")
        st.write(answer)

if __name__ == "__main__":
    main()
