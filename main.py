import sys

import uvicorn
import yaml
from fastapi import FastAPI

from app.index import *

app = FastAPI()

run_mode = sys.argv[1]

with open('constants.yaml', encoding='UTF-8') as f:
    constants = yaml.load(f, Loader=yaml.FullLoader)

with open('config.yaml', encoding='UTF-8') as f:
    configs = yaml.load(f, Loader=yaml.FullLoader)


@app.get("/")
async def root(video_id: str = '', lang: str = constants['default_language']):
    response = await index(video_id, lang)
    return response


if __name__ == "__main__":
    if run_mode == 'local':
        uvicorn.run(app, host=configs['host']['local'], port=configs['port']['local'])
    if run_mode == 'server':
        uvicorn.run(app, host=configs['host']['server'], port=configs['port']['server'])