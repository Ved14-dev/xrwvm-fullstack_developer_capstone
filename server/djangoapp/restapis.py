import os
from urllib.parse import quote

import requests
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")


def get_request(endpoint, **kwargs):
    response = requests.get(f"{backend_url}{endpoint}", timeout=10, **kwargs)
    response.raise_for_status()
    return response.json()


def analyze_review_sentiments(text):
    request_url = f"{sentiment_analyzer_url.rstrip('/')}/analyze/{quote(text)}"
    response = requests.get(request_url, timeout=10)
    response.raise_for_status()
    return response.json()


def post_review(data_dict):
    response = requests.post(
        f"{backend_url}/insert_review", json=data_dict, timeout=10
    )
    response.raise_for_status()
    return response.json()
