# Finance_app.py
from dotenv import load_dotenv
import streamlit as st
import os
import base64
import io
from PIL import Image
import pdf2image
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
    st.sidebar.title("GemInvest")
    st.sidebar.write("This application uses Gemini Pro Vision to analyze the uploaded financial portfolio and provide insights based on the user's investment goals by Highlighting potential risks, growth opportunities, and giving a general health check of the portfolio")
    st.sidebar.write("## How to Use")
    st.sidebar.write("""
        - Write a brief description of investment goals.
        - Upload your financial portfolio as PDF
        - Click the 'Analyze Portfolio' button to see the result.
    """)

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, pdf_content, input_text):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, pdf_content[0], input_text])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [{"mime_type": "image/jpeg", "data": base64.b64encode(img_byte_arr).decode()}]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

def main():
    load_sidebar_content()
    st.header("GemInvest")

    input_text = st.text_area("Brief description of investment goals:", key="input")
    uploaded_file = st.file_uploader("Upload your financial portfolio (PDF)...", type=["pdf"])

    if uploaded_file is not None:
        st.write("Portfolio Uploaded Successfully")

    analyze_button = st.button("Analyze Portfolio")

    input_prompt_analysis = """
    You are a sophisticated financial analyst with extensive experience in portfolio management and investment strategies. 
    Analyze the uploaded financial portfolio and provide insights based on the user's investment goals. 
    Highlight potential risks, growth opportunities, and give a general health check of the portfolio.
    """

    if analyze_button and uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt_analysis, pdf_content, input_text)
        st.subheader("Analysis Results")
        st.write(response)

if __name__ == "__main__":
    main()
