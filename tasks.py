import celery
import os

app = celery.Celery('tasks')
app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])

@app.task
def count(text):
    print(len(text))
    return len(text)

