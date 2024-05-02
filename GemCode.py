# CodeGenerator_app.py
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
    st.sidebar.title("GemCode")
    st.sidebar.write("This application uses gemini-1.5-pro-latest to generate code based on your query")
    st.sidebar.write("## How to Use")
    st.sidebar.write("""
        - Select the programming language.
        - Enter your coding query or description
        - Click the 'Generate Code' button to see the result.
    """)

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_code(language, query):
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    # Create a detailed prompt to instruct the model to generate specific code.
    prompt = f"Write a {language} function based on this description: {query}. " \
             f"Include comments and handle typical edge cases. Provide an example on how to use the code."
    response = model.generate_content(prompt)
    return response.text

def main():
    load_sidebar_content()
    
    st.header("GemCode")

    # Allow users to specify the programming language
    language = st.selectbox("Select the programming language:", 
                            ["Python", "JavaScript", "Java", "C++", "Ruby", "Go", "Other"])
    query = st.text_area("Enter your coding query or description:")

    if st.button("Generate Code"):
        if query:
            generated_code = generate_code(language, query)
            st.session_state.generated_code = generated_code  # Store generated code in session state
            st.subheader("Generated Code")
            st.code(generated_code)  # Display generated code

if __name__ == "__main__":
    main()
