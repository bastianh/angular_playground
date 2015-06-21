from celery import Celery

app = Celery('tasks')
app.config_from_object('backend.settings')

@app.task
def add(x, y):
    return x + y
