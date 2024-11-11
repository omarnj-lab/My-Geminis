# Sentiment_analysis_app.py
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
    st.sidebar.title("GemMood")
    st.sidebar.write("This application uses Gemini Pro to perfom a sentiment analysis task.")
    st.sidebar.write("## How to Use")
    st.sidebar.write("""
        - Enter the text you want to analyze its setiment.
        - Click the 'Analyze Sentiment' button to see the result.
    """)

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def analyze_sentiment(text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Please analyze the sentiment of the following sentence: '{text}'. Indicate if the sentiment is positive, negative, or neutral. Provide the percentage of confidence in your assessment and identify any specific emotions or feelings expressed."
    response = model.generate_content(prompt)
    return response.text

def main():
    load_sidebar_content()
    st.header("GemMood")
    user_input = st.text_area("Enter a sentence:")
    if st.button("Analyze Sentiment"):
        sentiment = analyze_sentiment(user_input)
        st.subheader("Sentiment Analysis")
        st.write(sentiment)

if __name__ == "__main__":
    main()
