# MarketTrendAnalysis_app.py
import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv
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
    st.sidebar.title("GemTrend")
    st.sidebar.write("This application uses Gemini Pro to provide an analysis of the following market trends based on the dataset provided.")
    st.sidebar.write("## How to Use")
    st.sidebar.write("""
        - Upload your market data (CSV format).
        - Click the 'Analyze Trends' button to see the result.
    """)

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def analyze_market_trends(data):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Provide an analysis of the following market trends based on the dataset provided: {data.describe().to_string()}"
    response = model.generate_content(prompt)
    return response.text

def main():
    load_sidebar_content()
    st.header("GemTrend")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your market data (CSV format):", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("Data Uploaded Successfully!")
        st.write("Data Preview:")
        st.dataframe(data.head())

        if st.button("Analyze Trends"):
            st.write("Analyzing Data...")
            analysis = analyze_market_trends(data)
            st.subheader("Market Trends Analysis")
            st.write(analysis)

if __name__ == "__main__":
    main()
