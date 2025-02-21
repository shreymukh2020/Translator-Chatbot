
import os
import json
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# Configure OpenAI API key safely
try:
    working_dir = os.path.dirname(os.path.abspath(__file__))
    with open(f"{working_dir}/config.json") as f:
        config_data = json.load(f)
    OPENAI_API_KEY = config_data.get("OPENAI_API_KEY", "")
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key not found in config.json")
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
except Exception as e:
    st.error(f"Error loading OpenAI API key: {e}")

# Initialize OpenAI LLM with GPT-4o
llm = ChatOpenAI(model="gpt-4o", temperature=0, max_tokens=512)

def translate(input_language, output_language, input_text):
    """Translation function using LangChain."""
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant that translates {input_language} to {output_language}."),
            ("human", "{input}")
        ]
    )

    # Create LLMChain
    chain = LLMChain(llm=llm, prompt=prompt)

    # Run translation
    response = chain.run(
        {
            "input_language": input_language,
            "output_language": output_language,
            "input": input_text
        }
    )

    return response

# Streamlit UI setup
def main():
    # Page configuration
    st.set_page_config(page_title="Language Translation", page_icon="🌍", layout="wide")

    # Apply custom styling for red Clear Chat History button
    st.markdown("""
        <style>
            /* Sidebar Styling */
            [data-testid="stSidebar"] {
                background-color: #008080 !important;  
                color: white !important;
                padding: 20px;
                text-align: center;
            }

            /* Sidebar Text */
            .sidebar-icons {
                font-size: 22px;  
                font-weight: bold;
                color: white;
                text-align: center;
                margin-bottom: 10px;
            }

            .sidebar-desc {
                font-size: 18px;
                font-weight: bold;
                font-style: italic;
                color: #d9d9d9;
                text-align: center;
                margin-bottom: 20px;
            }

            /* Sidebar Labels */
            .stSelectbox label {
                font-size: 20px !important;
                font-weight: bold !important;
                color: white !important;
            }

            /* Red Clear Chat Button */
            .stButton>button {
                background-color: red !important;
                color: white !important;
                border-radius: 10px !important;
                padding: 12px 20px !important;
                font-size: 18px !important;
                font-weight: bold !important;
                border: none !important;
            }

            .stButton>button:hover {
                background-color: darkred !important;
            }

            /* Text Input */
            .stTextArea textarea, .stTextInput input {
                border-radius: 10px;
                border: 2px solid #008080;
                padding: 12px;
                font-size: 18px;
            }

            /* Response Box */
            .response-box {
                background-color: #f1f1f1;
                padding: 20px;
                border-radius: 10px;
                margin-top: 20px;
                font-size: 18px;
                font-weight: bold;
            }

            /* Header */
            .stTitle {
                font-size: 28px;
                color: #008080;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("🌍 Language Translation Assistant")

    # Initialize session state for translations
    if "translated_text" not in st.session_state:
        st.session_state.translated_text = ""
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    # Sidebar setup
    with st.sidebar:
        st.markdown("<div class='sidebar-icons'>你好 • नमस्ते • こんにちは • Bonjour • Hola</div>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-desc'>Break language barriers, one translation at a time!</div>", unsafe_allow_html=True)

        # Language selection
        input_language = st.selectbox("Select input language", 
            ["English", "Spanish", "French", "German", "Italian", "Portuguese", "Bengali", "Gujarati", "Chinese", "Japanese", "Arabic", "Persian", "Turkish"]
        )

        output_language = st.selectbox("Select output language", 
            ["English", "Spanish", "French", "German", "Italian", "Portuguese", "Bengali", "Gujarati", "Chinese", "Japanese", "Arabic", "Persian", "Turkish"]
        )

        # Clear Chat History Button (fully working)
        if st.button("Clear Chat History", key="clear_history"):
            st.session_state.translated_text = ""  # Clear stored translations
            st.session_state.user_input = ""  # Clear user input field
            st.experimental_rerun()  # Rerun app to reflect the changes

    # Main content area
    st.subheader("Enter the text to be translated:")
    user_input = st.text_area("Type your text here", height=150, value=st.session_state.user_input)

    if st.button("Translate"):
        if user_input.strip():
            with st.spinner("Translating..."):
                translated_text = translate(input_language, output_language, user_input)

            # Store and display translation
            st.session_state.translated_text = translated_text
            st.session_state.user_input = user_input
            st.markdown(f"<div class='response-box'><b>Translated Text:</b><br>{st.session_state.translated_text}</div>", unsafe_allow_html=True)
        else:
            st.warning("Please enter some text to translate.")

if __name__ == "__main__":
    main()
