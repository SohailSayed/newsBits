import celery
import os
import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer {}".format(os.getenv('INFERENCE_API_KEY'))}

app = celery.Celery('tasks')
app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

@app.task
def summarize(text: str, max_len: int) -> str:
    try:
        summary = query({"inputs" : text, "max_length" : max_len,})
        return summary[0]["summary_text"]
    except:
        return summarize(text=text[:(len(text) // 2)], max_len=max_len//2) + summarize(text=text[(len(text) // 2):], max_len=max_len//2)