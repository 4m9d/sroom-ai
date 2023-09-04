import sys
import threading
import uvicorn
import yaml
from fastapi import FastAPI
from celery.result import AsyncResult

from celery_app import celery_app
from app.index import *

app = FastAPI()

run_mode = sys.argv[1]

with open('constants.yaml', encoding='UTF-8') as f:
    constants = yaml.load(f, Loader=yaml.FullLoader)

with open('config.yaml', encoding='UTF-8') as f:
    configs = yaml.load(f, Loader=yaml.FullLoader)

task_list = []
thread_lock = threading.Lock()


@app.get("/", status_code=202)
async def root(video_id: str = '', lang: str = constants['default_language']):
    task = index.delay(video_id, lang)
    with thread_lock:
        task_list.append(task.id)
    return {"message": "submit success"}


@app.get("/results")
def result():
    global task_list
    new_task_list = []
    result_list = []

    with thread_lock:
        for task_id in task_list:
            task = AsyncResult(task_id, app=celery_app)
            if task.status == 'SUCCESS':
                result_list.append(task.result)
            else:
                new_task_list.append(task_id)

        response = result_list.copy()
        task_list = new_task_list
        result_list.clear()

        return {'results': response}


if __name__ == "__main__":
    if run_mode == 'local':
        uvicorn.run(app, host=configs['host']['local'], port=configs['port']['local'])
    if run_mode == 'server':
        uvicorn.run(app, host=configs['host']['server'], port=configs['port']['server'])