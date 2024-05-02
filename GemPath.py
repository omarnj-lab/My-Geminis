# LearningPathwayGenerator_app.py
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
    st.sidebar.title("GemPath")
    st.sidebar.write("This application uses gemini-1.5-pro-latest to Create a detailed learning roadmap for a student interested in a certain major")
    st.sidebar.write("## How to Use")
    st.sidebar.write("""
        - Enter the major or field of study
        - Describe your specific learning goals or interests
        - Click the 'Generate Learning Pathway' button to see the result.
    """)
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_learning_pathway(major, details):
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    # Create a detailed prompt to instruct the model to generate a learning pathway.
    prompt = f"Create a detailed learning roadmap for a student interested in {major}. " \
             f"Include key subjects to study, recommended resources (books, websites, courses), " \
             f"and essential tips for effective learning. Focus on: {details}"
    response = model.generate_content(prompt)
    return response.text

def main():
    load_sidebar_content()
    st.header("GemPath")

    major = st.text_input("Enter the major or field of study:")
    details = st.text_area("Describe your specific learning goals or interests:")

    if st.button("Generate Learning Pathway"):
        if major and details:
            learning_pathway = generate_learning_pathway(major, details)
            st.session_state.learning_pathway = learning_pathway  # Store the generated pathway in session state
            st.subheader("Custom Learning Pathway")
            st.write(learning_pathway)  # Display the generated learning pathway

if __name__ == "__main__":
    main()
