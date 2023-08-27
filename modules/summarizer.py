from transformers import pipeline
from dotenv import load_dotenv
import os
import requests

def summarize_text(text: str, max_len: int) -> str:
    try:
        response = query({"inputs" : text, "max_length" : max_len,})
        if not response.ok:
            return "Condensed.news is currently experiening some issues in the backend. After being resolved, article summaries will display here again within the next two hours. I appreciate your patience!"
        summary = response.json()
        return summary[0]["summary_text"]
    except Exception as e:
        print(e)
        return summarize_text(text=text[:(len(text) // 2)], max_len=max_len//2) + summarize_text(text=text[(len(text) // 2):], max_len=max_len//2)

def query(payload):
    load_dotenv()

    headers = {"Authorization": "Bearer {}".format(os.getenv('INFERENCE_API_KEY'))}
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    response = requests.post(API_URL, headers=headers, json=payload)
    return response

