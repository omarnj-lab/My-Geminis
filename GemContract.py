# ContractAnalysis_app.py
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
    
    st.sidebar.image(f"data:image/png;base64,{encoded_logo}", use_container_width=True)
    st.sidebar.title("GemContract")
    st.sidebar.write("This application uses Gemini Pro Vision to analyze the uploaded contract and extract key clauses, terms, obligations, and compliance details.")
    st.sidebar.write("## How to Use")
    st.sidebar.write("""
        - Upload your contract document (PDF)
        - After The analysis, you may ask any specific question question about the contract  
        - Click the 'Get Answer' button to see the result.
    """)

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, pdf_content):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_prompt, pdf_content[0]])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [{"mime_type": "image/jpeg", "data": base64.b64encode(img_byte_arr).decode()}]
        return pdf_parts, img_byte_arr
    else:
        raise FileNotFoundError("No file uploaded")

def main():
    load_sidebar_content()
    
    st.header("GemContract")

    uploaded_file = st.file_uploader("Upload your contract document (PDF)...", type=["pdf"])
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file  # Save uploaded file to session state

    if 'uploaded_file' in st.session_state:
        st.write("Contract Document Uploaded Successfully")
        if 'pdf_content' not in st.session_state or 'img_content' not in st.session_state:
            st.session_state.pdf_content, st.session_state.img_content = input_pdf_setup(st.session_state.uploaded_file)
        
        submit_analysis = st.button("Analyze Contract")
        if submit_analysis or 'analysis_response' in st.session_state:
            if 'analysis_response' not in st.session_state:
                input_prompt = """
                Analyze the uploaded contract and extract key clauses, terms, obligations, and compliance details. Summarize the important elements of the contract.
                """
                st.session_state.analysis_response = get_gemini_response(input_prompt, st.session_state.pdf_content)
            
            st.subheader("GemContract")
            st.write(st.session_state.analysis_response)

            # Allow asking questions about the contract
            question = st.text_input("Ask a question about the contract:")
            if st.button("Get Answer") and question:
                answer_prompt = f"Based on the contract: {st.session_state.analysis_response} \n\nQuestion: {question} \nAnswer:"
                answer = get_gemini_response(answer_prompt, st.session_state.pdf_content)
                st.subheader("Answer to Your Question")
                st.write(answer)

if __name__ == "__main__":
    main()
