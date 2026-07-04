import requests
import os

import streamlit as st

NEWS_API_KEY = st.secrets["NEWS_API_KEY"]

def get_news(topic):
    url = "https://newsapi.org/v2/everything"

    params = {
        "q": topic,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(url, params=params)

    data = response.json()

    articles = []

    for article in data.get("articles", []):
        articles.append({
            "title": article["title"],
            "description": article["description"],
            "source": article["source"]["name"],
            "url": article["url"]
        })

    return articles