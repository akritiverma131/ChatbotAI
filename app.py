import streamlit as st
import json
import os
from datetime import datetime
from difflib import get_close_matches
import nltk
from nltk.tokenize import word_tokenize

st.set_page_config(
    page_title="Chatbot AI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Chatbot AI")
st.write("Hello! Welcome to my AI Chatbot.")
st.write("Ask me anything about Python, AI, Machine Learning, and more!")

knowledge = {
    "hello": "Hello! How can I help you today?",
    "hi": "Hi! Nice to meet you.",
    "how are you": "I am fine! Thanks for asking.",
    "what is ai": "AI stands for Artificial Intelligence. It enables computers to perform intelligent tasks.",
    "what is machine learning": "Machine Learning is a branch of AI that allows computers to learn patterns from data.",
    "what is deep learning": "Deep Learning uses neural networks to learn from data.",
    "what is python": "Python is a popular programming language known for its simple syntax.",
    "what is nlp": "NLP stands for Natural Language Processing. It helps computers understand human language.",
    "what is computer vision": "Computer Vision helps computers understand images and videos.",
    "what is data science": "Data Science involves collecting, analyzing, and interpreting data.",
    "what is dbms": "DBMS stands for Database Management System. It is used to store and manage data.",
    "what is cloud computing": "Cloud Computing provides computing services over the internet.",
    "what is aws": "AWS stands for Amazon Web Services. It provides cloud computing services.",
    "bye": "Goodbye! Have a great day!",
    "thank you": "You're welcome! Happy to help."
}

def get_response(message):
    message = message.lower().strip()

    if message in knowledge:
        return knowledge[message]

    matches = get_close_matches(
        message,
        knowledge.keys(),
        n=1,
        cutoff=0.6
    )

    if matches:
        return knowledge[matches[0]]

    words = set(message.split())

    for question, answer in knowledge.items():
        if words.intersection(set(question.split())):
            return answer

    return "Sorry, I don't know the answer yet. Please try asking about Python, AI, NLP, or Machine Learning."

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    response = get_response(user_input)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    with st.chat_message("assistant"):
        st.write(response)

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
