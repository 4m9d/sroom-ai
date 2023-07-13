import uvicorn
import yaml
from fastapi import FastAPI

from app.index import *

app = FastAPI()

with open('constants.yaml', encoding='UTF-8') as f:
    constants = yaml.load(f, Loader=yaml.FullLoader)

with open('config.yaml', encoding='UTF-8') as f:
    configs = yaml.load(f, Loader=yaml.FullLoader)


@app.get("/")
async def root(video_id: str = '', lang: str = constants['default_language']):
    print(video_id, lang)
    response = await index(video_id, lang)
    return response


if __name__ == "__main__":
    uvicorn.run(app, host=configs['host']['local'], port=configs['port']['local'])
