import streamlit as st
from langchain_community.callbacks import StreamlitCallbackHandler
from streamlit_chat import message
from typing import Annotated
from typing_extensions import TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from graph import graph

st.set_page_config(
    page_title="LangChain Chatbot",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Streamlit app to run chatbot
st_callback = StreamlitCallbackHandler(st.container())

# Stream updates from LangGraph
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'pending_input' not in st.session_state:
    st.session_state['pending_input'] = ""

# Custom CSS to style the chatbot interface like the provided UI
st.markdown(
    """
    <style>
    .user-message {
        background-color: #DCF8C6;
        border-radius: 20px;
        padding: 10px;
        margin-bottom: 10px;
        max-width: 60%;
        align-self: flex-end;
    }
    .assistant-message {
        background-color: #F1F0F0;
        border-radius: 20px;
        padding: 10px;
        margin-bottom: 10px;
        max-width: 60%;
        align-self: flex-start;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the chat history using streamlit_chat library
chat_placeholder = st.empty()
with chat_placeholder.container():
    for message_data in st.session_state.chat_history:
        if message_data['role'] == 'user':
            message(message_data['content'], is_user=True)
        else:
            message(message_data['content'])

# Define the submit callback function
def submit_message():
    user_input = st.session_state.pending_input
    if user_input:
        # Append user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        prompt = user_input
        # Get assistant response and append to chat history
        for event in graph.stream({"messages": [("user", prompt)]}):
            for value in event.values():
                st.session_state.chat_history.append({"role": "assistant", "content": value["messages"][-1].content})
        # Clear the input field after submission
        st.session_state.pending_input = ""

# Text input for user messages with on_change callback
st.text_input("Message:", key="pending_input", on_change=submit_message)
