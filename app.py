import os
import json
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# Configure OpenAI API key
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
OPENAI_API_KEY = config_data["OPENAI_API_KEY"]
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Initialize OpenAI LLM with GPT-4 model
llm = ChatOpenAI(model="gpt-4", temperature=0)

def translate(input_language, output_language, input_text):
    # Define the prompt template for translation
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant that translates {input_language} to {output_language}."), 
            ("human", "{input}")
        ]
    )

    # Create the LLMChain with the prompt and the OpenAI model
    chain = LLMChain(llm=llm, prompt=prompt)

    # Run the chain with the input values
    response = chain.run(
        {
            "input_language": input_language,
            "output_language": output_language,
            "input": input_text
        }
    )

    return response

# Streamlit UI with enhancements
def main():
    # Set page configuration for a better look
    st.set_page_config(page_title="Language Translation", page_icon="🌍", layout="wide")

    # Apply custom CSS styles
    st.markdown("""
        <style>
            /* Sidebar Styling */
            [data-testid="stSidebar"] {
                background-color: #008080 !important;  /* Teal color */
                color: white !important;
                padding: 20px;
                text-align: center;
            }

            /* Sidebar Language Icons */
            .sidebar-icons {
                font-size: 22px;  /* Reduced size from 28px to 22px */
                font-weight: bold;
                color: white;
                text-align: center;
                margin-bottom: 10px;
            }

            /* Sidebar Tagline */
            .sidebar-desc {
                font-size: 18px;
                font-weight: bold;
                font-style: italic;
                color: #d9d9d9; /* Light gray */
                text-align: center;
                margin-bottom: 20px;
            }

            /* Sidebar Labels */
            .stSelectbox label {
                font-size: 20px !important;
                font-weight: bold !important;
                color: white !important;
            }

            /* Button Styling */
            .stButton>button {
                background-color: #008080;  /* Teal color */
                color: white;  /* White text */
                border-radius: 10px;
                padding: 12px 20px;
                font-size: 18px;
                font-weight: bold;
                border: none;
            }

            .stButton>button:hover {
                background-color: #006666;  /* Darker teal on hover */
            }

            /* Clear Chat History Button */
            .clear-button {
                background-color: red !important; /* Red button */
                color: white !important; /* White text */
                border-radius: 10px;
                padding: 12px 20px;
                font-size: 18px;
                font-weight: bold;
                border: none;
                cursor: pointer;
            }

            /* Text Input Styling */
            .stTextArea textarea, .stTextInput input {
                border-radius: 10px;
                border: 2px solid #008080;
                padding: 12px;
                font-size: 18px;
            }

            /* Response Box Styling */
            .response-box {
                background-color: #f1f1f1;
                padding: 20px;
                border-radius: 10px;
                margin-top: 20px;
                font-size: 18px;
                font-weight: bold;
            }

            /* Header & Title */
            .stTitle {
                font-size: 28px;
                color: #008080;
            }

            .stMarkdown {
                font-size: 18px;
                color: #333;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("🌍 Language Translation Assistant")

    # Sidebar content
    with st.sidebar:
        st.markdown("<div class='sidebar-icons'>你好 • नमस्ते • こんにちは • Bonjour • Hola</div>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-desc'>Break language barriers, one translation at a time!</div>", unsafe_allow_html=True)

        # Dropdown menu for selecting input and output languages
        input_language = st.selectbox(
            "Select input language", 
            [
                "English", "Spanish", "French", "German", "Italian", 
                "Portuguese", "Bengali", "Gujarati", "Chinese", 
                "Japanese", "Arabic", "Persian", "Turkish"
            ]
        )

        output_language = st.selectbox(
            "Select output language", 
            [
                "English", "Spanish", "French", "German", "Italian", 
                "Portuguese", "Bengali", "Gujarati", "Chinese", 
                "Japanese", "Arabic", "Persian", "Turkish"
            ]
        )

        # Clear Chat History Button
        if st.button("Clear Chat History", key="clear_history"):
            st.session_state.translated_text = ""  # Clear any stored translation history
            st.markdown("<div style='color: white; font-weight: bold;'>Cleared chat history, start afresh!</div>", unsafe_allow_html=True)

    # Main content area for user input
    st.subheader("Enter the text to be translated:")

    user_input = st.text_area("Type your text here", height=150)

    if st.button("Translate"):
        if user_input.strip():
            # Translate the input text
            translated_text = translate(input_language, output_language, user_input)

            # Display the translated text
            st.markdown(f"<div class='response-box'><b>Translated Text:</b><br>{translated_text}</div>", unsafe_allow_html=True)
        else:
            st.warning("Please enter some text to translate.")

if __name__ == "__main__":
    main()
