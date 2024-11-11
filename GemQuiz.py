# ExamGenerator_app.py
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
    
    st.sidebar.image(f"data:image/png;base64,{encoded_logo}", use_container_width=True)
    st.sidebar.title("GemQuiz")
    st.sidebar.write("This application uses Gemini Pro to generate quiz questions and answers on the topic of a certain subject")
    st.sidebar.write("## How to Use")
    st.sidebar.write("""
        - Enter the subject
        - Enter the specific topic
        - Select the type of questions
        - Click the 'Generate Quiz' button to see the result.
    """)

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_exam_questions(subject, topic, question_type, number_of_questions):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Generate {number_of_questions} {question_type} questions and answers on the topic '{topic}' in the subject '{subject}'."
    response = model.generate_content(prompt)
    return response.text

def main():
    load_sidebar_content()
    st.header("GemQuiz")

    # User inputs for subject and topic
    subject = st.text_input("Enter the subject:")
    topic = st.text_input("Enter the specific topic:")
    
    # Dropdown for selecting the type of questions
    question_types = ["Multiple Choice", "True/False", "Short Answer", "Essay"]
    question_type = st.selectbox("Select the type of questions:", question_types)
    
    # Number of questions
    number_of_questions = st.number_input("Number of questions:", min_value=1, max_value=50, value=10)

    if st.button("Generate Quiz"):
        if topic and subject:
            exam_questions = generate_exam_questions(subject, topic, question_type, number_of_questions)
            st.subheader("Generated Exam Questions")
            st.write(exam_questions)
        else:
            st.error("Please enter both subject and topic.")

if __name__ == "__main__":
    main()
