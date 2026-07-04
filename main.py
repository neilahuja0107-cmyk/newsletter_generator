from groq import Groq
from dotenv import load_dotenv
import os
import streamlit as st
import requests

from prompts import SYSTEM_PROMPT
from news import get_news

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


if "newsletter" not in st.session_state:
    st.session_state.newsletter = ""

if "generated" not in st.session_state:
    st.session_state.generated = False

st.title("Newsletter Generator")

st.write(
    "This is a simple newsletter generator that uses the Groq API "
    "to generate content based on your preferences."
)

st.write("Select a topic and newsletter style below.")

topic = st.selectbox(
    "Choose Desired Topic",
    [
        "Startups",
        "AI",
        "Crypto",
        "Cybersecurity",
        "Programming",
        "Technology"
    ]
)

style = st.selectbox(
    "Choose Newsletter Style",
    [
        "Professional",
        "Conversational",
        "Minimal & Concise",
        "Analytical",
        "Professional but Witty"
    ]
)


if st.button("Generate Newsletter"):

    with st.spinner("Generating Newsletter Content..."):

        system_prompt = SYSTEM_PROMPT.format(
            topic=topic,
            style=style,
            articles=get_news(topic)
        )

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": system_prompt
                }
            ],
            max_tokens=1000
        )

        st.session_state.newsletter = response.choices[0].message.content
        st.session_state.generated = True


if st.session_state.generated:

    st.text_area(
        "Happy Reading!",
        value=st.session_state.newsletter + "\n\n...",
        height=400
    )

    st.write(
        "🔒 This is a preview of the newsletter. "
        "To enjoy reading the full newsletter, "
        "please subscribe to our email newsletter service."
    )

    email = st.text_input(
        "Enter your email"
    )

    if st.button("Send Full Newsletter"):

        if email.strip() == "":
            st.warning("Please enter your email.")

        else:

            try:

                response = requests.post(
                    "https://newsletter-generator-43nz.onrender.com/send-email",
                    json={
                        "receiver": email,
                        "newsletter": st.session_state.newsletter+ "\n\nThanks for reading!",
                        "topic": topic
                    }
                )

                if response.status_code == 200:
                    st.success("Newsletter sent successfully! 📧")
                    st.text("Please check your inbox (and spam folder) for the newsletter.")

                else:
                    st.error(response.text)

            except Exception as e:
                st.error(f"Error: {e}")