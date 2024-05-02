import streamlit as st
import subprocess
import sys

# Setting the page configuration
st.set_page_config(page_title="Multi-Function App", layout="wide")

# Custom styles
def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load custom CSS styles
local_css("style.css")


st.markdown("""
<style>
.markdown-text-container, .stMarkdown {
    text-align: left;
    font-family: 'Georgia', serif;
    font-size: 20px;
    color: #94506B;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
}
.element-container {
    font-family: 'Courier New', monospace;
    color: #e76f51;
    font-size: 18px;
    text-align: center;
    text-shadow: 0px 2px 3px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

# Convenience function to change label style using inline CSS
def change_label_style(label, style):
    html = f"""
    <style>
        {label} {{
            {style}
        }}
    </style>
    """
    st.components.v1.html(html)


# Main interface layout
col1, col2, col3 = st.columns([1,2,1])

# Sidebar
#with st.sidebar:
#    st.markdown("# Sidebar")
#    st.markdown("Welcome to the sidebar!")
    # You can add additional elements to the sidebar here

with col2:
    st.image("logo.png", width=400, )  # Adjust width as needed
    
    # Row 1: Basic NLP Tasks
    st.markdown("#### ✥ Gemini Language Wizards 🧙‍♂️ ")
    st.markdown("Explore the power of language with Gemini's NLP tools.")
    cols = st.columns(4)
    nlp_apps = ["Geminize", "GemQuest", "GemMood", "GemLingo"]
    nlp_commands = ["Geminize.py", "GemQuest.py", "GemMood.py", "GemLingo.py"]
    for i, app in enumerate(nlp_apps):
        if cols[i].button(app):
            subprocess.run([f"{sys.executable}", "Geminize.py"])
    
    # Row 2: Professional Systems
    st.markdown("#### ✥ Gemini Enterprise Engines 🚀")
    st.markdown("Drive your business forward with Gemini's professional systems.")
    cols = st.columns(4)
    professional_apps = ["GemResume", "GemInvest", "GemTrend", "GemContract"]
    professional_commands = ["GemResume.py", "GemInvest.py", "GemTrend.py", "GemContract.py"]
    for i, app in enumerate(professional_apps):
        if cols[i].button(app):
            subprocess.run([f"{sys.executable}", professional_commands[i]])
    
    # Row 3: Educational Enhancements
    st.markdown("#### ✥ Gemini Academic Tools 🏛️")
    st.markdown("Enhance your learning experience with Gemini's educational tools.")
    cols = st.columns(4)
    educational_apps = ["GemSolve", "GemQuiz", "GemCode", "GemPath"]
    educational_commands = ["GemSolve.py", "GemQuiz.py", "GemCode.py", "GemPath.py"]
    for i, app in enumerate(educational_apps):
        if cols[i].button(app):
            if educational_commands[i]:
                subprocess.run([f"{sys.executable}", educational_commands[i]])
            else:
                st.write(f"Functionality for {app} is not implemented yet.")
    
    # Row 4: Multimodal Applications
    st.markdown("#### ✥ Gemini Media Mixers 🎬")
    st.markdown("Dive into multimedia exploration with Gemini's versatile applications.")
    cols = st.columns(4)
    multimodal_apps = ["GemTex", "GemPix", "GemReel", "GemEcho"]
    multimodal_commands = ["GemTex.py", "GemPix.py", "GemReel.py", "GemEcho.py"]
    for i, app in enumerate(multimodal_apps):
        if cols[i].button(app):
            if multimodal_commands[i]:
                subprocess.run([f"{sys.executable}", multimodal_commands[i]])
            else:
                st.write(f"Functionality for {app} is not implemented yet.")
    
    st.markdown("#### ✥ Craft Your Concept ✏️")
    st.markdown("Create your own custom app tailored to your unique needs.")
    if st.button("Create Your Own App", key="create_app"):
        subprocess.run([f"{sys.executable}", "GemCustom.py"])


# Adding an informational message at the bottom
st.info("Discover a diverse range of applications tailored to your needs with My Geminis. Whether you're delving into language processing, powering through professional tasks, enhancing your educational experience, or exploring multimodal applications, My Geminis has you covered. Simply select a category below to unlock a world of possibilities!")
st.info("Created By Omer Nacar | 🔗 www.omarai.co")
