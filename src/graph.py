import os
import streamlit as st
from typing import Annotated
from typing_extensions import TypedDict
from langchain_groq import ChatGroq  # Updated import to use ChatGroq
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

# Define the state with message annotations
class State(TypedDict):
    messages: Annotated[list, add_messages]

groq_api_key = st.secrets["GROQ_API_KEY"]
# Initialize GroqModel model with streaming enabled
llm = ChatGroq(api_key=groq_api_key, model_name='llama-3.1-8b-instant', temperature=0, )

# Define the chatbot function
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# Build the LangGraph workflow
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.set_entry_point("chatbot")
graph_builder.set_finish_point("chatbot")
graph = graph_builder.compile()
