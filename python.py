import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
from difflib import get_close_matches
import json
import os

import nltk
from nltk.tokenize import word_tokenize


# NLTK
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)


# =====================================================
# MEMORY
# =====================================================

MEMORY_FILE = "memory.json"


def load_memory():

    if os.path.exists(MEMORY_FILE):

        with open(MEMORY_FILE, "r") as file:
            return json.load(file)

    return {}


def save_memory():

    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)


memory = load_memory()


# =====================================================
# CHAT HISTORY
# =====================================================

HISTORY_FILE = "chat_history.json"


def load_history():

    if os.path.exists(HISTORY_FILE):

        with open(HISTORY_FILE, "r") as file:
            return json.load(file)

    return []


def save_history():

    with open(HISTORY_FILE, "w") as file:
        json.dump(chat_history, file, indent=4)


chat_history = load_history()


# =====================================================
# KNOWLEDGE BASE
# =====================================================

knowledge = {

    "hadoop":
        "Hadoop is an open-source framework used to store and process large amounts of data.",

    "mongodb":
        "MongoDB is a NoSQL database that stores data in flexible JSON-like documents.",

    "python":
        "Python is a high-level programming language used in AI, Machine Learning, Data Science and Web Development.",

    "artificial intelligence":
        "Artificial Intelligence, or AI, allows computers to perform tasks that normally require human intelligence.",

    "ai":
        "AI stands for Artificial Intelligence. It enables computers to perform intelligent tasks.",

    "machine learning":
        "Machine Learning is a branch of AI that allows computers to learn patterns from data.",

    "deep learning":
        "Deep Learning is a part of Machine Learning that uses neural networks.",

    "computer vision":
        "Computer Vision helps computers understand and analyze images and videos.",

    "data science":
        "Data Science is the process of collecting, analyzing and interpreting data.",

    "dbms":
        "DBMS stands for Database Management System. It is used to store and manage data.",

    "cloud computing":
        "Cloud Computing provides computing services such as storage, servers and databases over the internet.",

    "aws":
        "AWS stands for Amazon Web Services. It provides cloud computing services.",

    "html":
        "HTML is used to create the structure of web pages.",

    "css":
        "CSS is used to design and style web pages.",

    "javascript":
        "JavaScript is used to make web pages interactive.",

    "chatbot":
        "A chatbot is a computer program that communicates with users."
}


# =====================================================
# BASIC RESPONSES
# =====================================================

responses = {

    "hello":
        "Hello! How can I help you?",

    "hi":
        "Hi! Nice to meet you.",

    "hey":
        "Hey! How are you?",

    "what is your name":
        "My name is Nova. I am your AI chatbot.",

    "who are you":
        "I am Nova, a Python-based AI chatbot.",

    "how are you":
        "I am fine! Thank you for asking.",

    "thank you":
        "You're welcome!",

    "thanks":
        "You're welcome!",

    "bye":
        "Goodbye! Have a nice day!"
}


# =====================================================
# GET RESPONSE
# =====================================================

def get_response(user_message):

    user_message = user_message.lower().strip()

    words = word_tokenize(user_message)

    print("User words:", words)


    # Remember name

    if "my name is" in user_message:

        name = user_message.split("my name is", 1)[1].strip()

        memory["name"] = name.title()

        save_memory()

        return "Nice to meet you, " + memory["name"] + "!"


    # Ask name

    if "what is my name" in user_message:

        if "name" in memory:

            return "Your name is " + memory["name"] + "."

        return "You have not told me your name yet."


    # Remember college

    if "i study at" in user_message:

        college = user_message.split("i study at", 1)[1].strip()

        memory["college"] = college.title()

        save_memory()

        return "Okay! I will remember that you study at " + memory["college"] + "."


    # Ask college

    if "where do i study" in user_message:

        if "college" in memory:

            return "You study at " + memory["college"] + "."

        return "You have not told me your college yet."


    # Knowledge base

    for topic, answer in knowledge.items():

        if topic in user_message:

            return answer


    # Basic responses

    if user_message in responses:

        return responses[user_message]


    # Similar questions

    questions = list(responses.keys())

    match = get_close_matches(
        user_message,
        questions,
        n=1,
        cutoff=0.5
    )

    if match:

        return responses[match[0]]


    # Time

    if "time" in words:

        current_time = datetime.now().strftime("%I:%M %p")

        return "The current time is " + current_time


    return "Sorry, I don't understand that yet."


# =====================================================
# THINKING EFFECT
# =====================================================

def show_response(user_message):

    response = get_response(user_message)

    # Remove thinking message
    chat_box.delete("end-3l", "end")

    # Bot response

    chat_box.insert(
        tk.END,
        "Nova 🤖\n",
        "bot_name"
    )

    chat_box.insert(
        tk.END,
        response + "\n\n",
        "bot_message"
    )

    # Save history

    chat_history.append({
        "user": user_message,
        "bot": response
    })

    save_history()

    chat_box.see(tk.END)


# =====================================================
# SEND MESSAGE
# =====================================================

def send_message(event=None):

    user_message = entry.get().strip()

    if user_message == "":
        return


    # User message

    chat_box.insert(
        tk.END,
        "You\n",
        "user_name"
    )

    chat_box.insert(
        tk.END,
        user_message + "\n\n",
        "user_message"
    )


    # Thinking message

    chat_box.insert(
        tk.END,
        "Nova 🤖\n",
        "bot_name"
    )

    chat_box.insert(
        tk.END,
        "Thinking...\n",
        "bot_message"
    )

    chat_box.see(tk.END)

    entry.delete(0, tk.END)

    # Wait 700 milliseconds
    root.after(
        700,
        lambda: show_response(user_message)
    )


# =====================================================
# CLEAR CHAT
# =====================================================

def clear_chat():

    chat_box.delete("1.0", tk.END)

    chat_box.insert(
        tk.END,
        "Nova 🤖\n",
        "bot_name"
    )

    chat_box.insert(
        tk.END,
        "Hello! I am Nova. How can I help you?\n\n",
        "bot_message"
    )


# =====================================================
# MAIN WINDOW
# =====================================================

root = tk.Tk()

root.title("Nova AI Chatbot")

root.geometry("650x700")

root.configure(bg="#eaf4ff")


# =====================================================
# TITLE
# =====================================================

title = tk.Label(
    root,
    text="🤖 Nova AI",
    font=("Arial", 25, "bold"),
    bg="#eaf4ff",
    fg="#1f4e79"
)

title.pack(pady=(15, 5))


# =====================================================
# SUBTITLE
# =====================================================

subtitle = tk.Label(
    root,
    text="Your Personal AI Chatbot",
    font=("Arial", 11),
    bg="#eaf4ff",
    fg="#555555"
)

subtitle.pack(pady=(0, 10))


# =====================================================
# CHAT BOX
# =====================================================

chat_box = scrolledtext.ScrolledText(
    root,
    width=65,
    height=28,
    font=("Arial", 11),
    wrap=tk.WORD,
    bg="white",
    relief=tk.FLAT
)

chat_box.pack(
    padx=20,
    pady=10,
    fill=tk.BOTH,
    expand=True
)


# =====================================================
# TEXT STYLES
# =====================================================

chat_box.tag_config(
    "user_name",
    font=("Arial", 11, "bold")
)

chat_box.tag_config(
    "user_message",
    font=("Arial", 11)
)

chat_box.tag_config(
    "bot_name",
    font=("Arial", 11, "bold")
)

chat_box.tag_config(
    "bot_message",
    font=("Arial", 11)
)


# =====================================================
# WELCOME
# =====================================================

chat_box.insert(
    tk.END,
    "Nova 🤖\n",
    "bot_name"
)

chat_box.insert(
    tk.END,
    "Hello! I am Nova. How can I help you?\n\n",
    "bot_message"
)


# =====================================================
# BOTTOM FRAME
# =====================================================

bottom_frame = tk.Frame(
    root,
    bg="#eaf4ff"
)

bottom_frame.pack(
    fill=tk.X,
    padx=20,
    pady=15
)


# =====================================================
# INPUT
# =====================================================

entry = tk.Entry(
    bottom_frame,
    font=("Arial", 13),
    relief=tk.FLAT
)

entry.pack(
    side=tk.LEFT,
    fill=tk.X,
    expand=True,
    ipady=10,
    padx=(0, 10)
)


# =====================================================
# SEND BUTTON
# =====================================================

send_button = tk.Button(
    bottom_frame,
    text="Send",
    font=("Arial", 11, "bold"),
    bg="#1f6feb",
    fg="white",
    padx=18,
    pady=8,
    relief=tk.FLAT,
    command=send_message
)

send_button.pack(side=tk.LEFT)


# =====================================================
# CLEAR BUTTON
# =====================================================

clear_button = tk.Button(
    root,
    text="Clear Chat",
    font=("Arial", 10),
    command=clear_chat
)

clear_button.pack(pady=(0, 15))


# =====================================================
# ENTER KEY
# =====================================================

root.bind(
    "<Return>",
    send_message
)


# =====================================================
# START
# =====================================================

root.mainloop()