import asyncio
from celery_app import celery_app

from app.script import script, scriptService
from main import constants
from app.summary import summary
from app.quiz import quiz, quizv2


class ResponseModel:
    def __init__(self):
        self.video_id = ''
        self.summary = ''
        self.is_valid = 0
        self.quizzes = []

    def to_dict(self):
        return {
            'video_id': self.video_id,
            'is_valid': self.is_valid,
            'summary': self.summary,
            'quizzes': self.quizzes
        }


@celery_app.task()
def index(video_id: str = '', video_title: str = ''):
    response = ResponseModel()
    loop = asyncio.get_event_loop()

    youtube_script = script.Script()
    scriptService.get_script(youtube_script, video_id)

    response.video_id = video_id

    if youtube_script.is_valid:
        response.is_valid = 1

        summary_result = loop.run_until_complete(summary.generate_summary(youtube_script.text, video_title))
        quizzes_result = loop.run_until_complete(quizv2.generate_quizzes(summary_result))

        response.summary = summary_result
        response.quizzes = quizzes_result

    return response.to_dict()
