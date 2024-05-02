# SolutionChecker_app.py
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
    st.sidebar.title("GemSolve")
    st.sidebar.write("This application uses Gemini-1.5-pro-latest to solve questions based uploaded image of the question and your answer")
    st.sidebar.write("## How to Use")
    st.sidebar.write("""
        - Select the subject of your solution.
        - Upload an image of your question and solution
        - Click the 'Check My Answer' button to see the result.
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
    st.header("GemSolve")

    subject_options = ["Mathematics", "Physics", "Chemistry", "Biology", "History", "Geography"]
    subject = st.selectbox("Select the subject of your solution:", subject_options)
    
    uploaded_file = st.file_uploader("Upload an image of your question and solution:", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption='Uploaded Solution', use_column_width=True)
        st.write("Image Uploaded Successfully")

    if st.button("Check My Answer"):
        if uploaded_file:
            image_data = io.BytesIO(uploaded_file.getvalue())
            input_prompt = f"""
            Subject: {subject}
            Task: Analyze question and the solution presented in the image below. 
            1. Check all steps of the answer for correctness.
            2. Check all calculation is made correctly.
            3. Perform the necessary calculations to verify accuracy against the student's answer.
            4. Score the solution out of 5 based on accuracy and completeness.
            5. Provide detailed feedback explaining the score, noting any errors or omissions and suggesting improvements if necessary.
            """           
            response = get_gemini_response(input_prompt, image_data)
            st.subheader("Solution Feedback")
            st.write(response)
        else:
            st.error("Please upload an image containing your question and solution.")

if __name__ == "__main__":
    main()
