import sys
import os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from notebook.chef_service import ask_chef_agent

# Set up Page configuration
st.set_page_config(page_title="Personal Chef Assistant", page_icon="🍳", layout="centered")
st.title("🍳 Personal Chef Assistant")
st.subheader("Turn your leftover ingredients into delicious African recipes!")


# Initialize chat session history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I am your Personal Chef. To get started, what is your name? And do you have any dietary preferences, restrictions, or food allergies I should keep in mind?"
        }
    ]
    
    # Generate a unique thread ID for the agent memory session
    st.session_state.thread_id = "chef-streamlit-thread-1"


# Display existing chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if user_input := st.chat_input("What ingredients do you have?"):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Chef is cooking up ideas..."):
            try:
                
                text_response = ask_chef_agent(
                    user_input=user_input, 
                    thread_id=st.session_state.thread_id
                )

                st.markdown(text_response)
                st.session_state.messages.append({"role": "assistant", "content": text_response})

            except Exception as e:
                st.error(f"An error occurred: {e}")

# Fixed Footer below the chatbox
st.markdown(
    """
    <style>
    /* Fixed footer at the absolute bottom of the viewport */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        color: #888888;
        font-size: 0.8em;
        padding: 8px 0;
        z-index: 999;
        background-color: rgba(255, 255, 255, 0.0); /* Transparent */
    }
    
    /* Shift the floating chat input box up slightly so they don't overlap */
    div[data-testid="stChatInput"] {
        bottom: 32px !important;
    }
    </style>
    <div class="footer">
        Developed by <b>Inimfon Willie</b> | Inspired by 
        <b>Foundation: Introduction to LangChain - Python</b> course from LangChain Academy
    </div>
    """,
    unsafe_allow_html=True
)


