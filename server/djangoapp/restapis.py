import json
import os
from pathlib import Path
from urllib.parse import quote

import requests
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv("backend_url", "http://localhost:3030")
sentiment_analyzer_url = os.getenv("sentiment_analyzer_url", "http://localhost:5050/")
DATA_DIR = Path(__file__).resolve().parents[1] / "database" / "data"


def _fixture(name):
    with (DATA_DIR / name).open(encoding="utf-8") as file:
        return json.load(file)


def get_request(endpoint, **kwargs):
    try:
        response = requests.get(
            f"{backend_url.rstrip('/')}/{endpoint.lstrip('/')}", timeout=3, **kwargs
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        if endpoint == "fetchDealers":
            return _fixture("dealerships.json")["dealerships"]
        if endpoint.startswith("fetchDealers/"):
            state = endpoint.rsplit("/", 1)[-1].lower()
            return [
                dealer for dealer in _fixture("dealerships.json")["dealerships"]
                if dealer["state"].lower() == state
            ]
        if endpoint.startswith("fetchDealer/"):
            dealer_id = int(endpoint.rsplit("/", 1)[-1])
            return [
                dealer for dealer in _fixture("dealerships.json")["dealerships"]
                if dealer["id"] == dealer_id
            ]
        if endpoint.startswith("fetchReviews/dealer/"):
            dealer_id = int(endpoint.rsplit("/", 1)[-1])
            return [
                review for review in _fixture("reviews.json")["reviews"]
                if review["dealership"] == dealer_id
            ]
        return []


def analyze_review_sentiments(text):
    try:
        response = requests.get(
            f"{sentiment_analyzer_url.rstrip('/')}/analyze/{quote(text)}", timeout=3
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        words = set(text.lower().split())
        positive = {"fantastic", "excellent", "great", "good", "wonderful", "love"}
        negative = {"bad", "poor", "terrible", "awful", "hate"}
        sentiment = "positive" if words & positive else "negative" if words & negative else "neutral"
        return {"sentiment": sentiment}


def post_review(data_dict):
    try:
        response = requests.post(
            f"{backend_url.rstrip('/')}/insert_review", json=data_dict, timeout=3
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        reviews_path = DATA_DIR / "reviews.json"
        payload = _fixture("reviews.json")
        next_id = max((review["id"] for review in payload["reviews"]), default=0) + 1
        review = {"id": next_id, **data_dict}
        payload["reviews"].append(review)
        with reviews_path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)
        return review
