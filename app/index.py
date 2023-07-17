from app.script.scriptService import *
from main import constants
from app.gpt.gpt import *
from app.summary.summary import *
from app.quiz.quiz import *
import json


class ResponseModel:
    def __init__(self):
        self.video_id = ""
        self.summary = ""
        self.quizes = []

    def setResponse(self, video_id: str, summary: str, quizes: list):
        self.video_id = video_id
        self.summary = summary
        self.quizes = quizes


async def index(video_id: str = '', lang: str = constants['default_language']):
    youtube_script = Script()
    response = ResponseModel()
    get_script(youtube_script, video_id, lang)

    # GPT로부터 요약본 생성
    summary = generate_summary(youtube_script.text)

    # 생성한 요약본을 기준으로 GPT로부터 퀴즈 생성
    quizes = generate_quiz(summary)

    # GPT로 부터 받은 여러 정보들을 JSON 양식에 맞게 조합

    response.setResponse(video_id, summary, quizes)

    return response
