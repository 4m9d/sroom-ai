import sys
import threading
import time

import uvicorn
import yaml
from fastapi import FastAPI
from celery.result import AsyncResult

from app.index import *

app = FastAPI()

run_mode = sys.argv[1]

with open('constants.yaml', encoding='UTF-8') as f:
    constants = yaml.load(f, Loader=yaml.FullLoader)

with open('config.yaml', encoding='UTF-8') as f:
    configs = yaml.load(f, Loader=yaml.FullLoader)

success = 0
failure = 0
test_time = 0
task_list = []
thread_lock = threading.Lock()


@app.get("/", status_code=202)
async def root(video_id: str = '', video_title: str = ''):
    task = index.delay(video_id, video_title)
    with thread_lock:
        task_list.append(task.id)
    return {"message": "submit success"}


@app.get("/results")
def result():

    global task_list
    global success
    global failure

    new_task_list = []
    result_list = []

    with thread_lock:
        for task_id in task_list:
            task = AsyncResult(task_id, app=celery_app)
            if task.status == 'SUCCESS':
                result_list.append(task.result)
                success += 1
            elif task.status == 'FAILURE':
                failure += 1
            else:
                new_task_list.append(task_id)

        response = result_list.copy()
        task_list = new_task_list
        result_list.clear()

        return {'results': response}


@app.post("/test_start")
async def test_start():
    global success
    global failure
    global test_time

    success = 0
    failure = 0
    test_time = time.time()

    return {"message": "test start"}


@app.get("/test_data")
def test_get():
    global task_list
    global success
    global failure

    new_task_list = []

    with thread_lock:
        for task_id in task_list:
            task = AsyncResult(task_id, app=celery_app)
            if task.status == 'SUCCESS':
                success += 1
            elif task.status == 'FAILURE':
                failure += 1
            else:
                new_task_list.append(task_id)

        task_list = new_task_list

    return {"success": success, "failure": failure, "time": time.time()-test_time}


if __name__ == "__main__":
    if run_mode == 'local':
        uvicorn.run(app, host=configs['host']['local'], port=configs['port']['local'])
    if run_mode == 'server':
        uvicorn.run(app, host=configs['host']['server'], port=configs['port']['server'])