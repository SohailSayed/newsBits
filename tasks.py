import celery
import os
from transformers import pipeline

app = celery.Celery('tasks')
app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])

@app.task
def summarize(text: str, max_len: int) -> str:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    try:
        summary = summarizer(text, max_length=max_len, min_length=10, do_sample=False)
        return summary[0]["summary_text"]
    except:
        return summarize(text=text[:(len(text) // 2)], max_len=max_len//2) + summarize(text=text[(len(text) // 2):], max_len=max_len//2)

