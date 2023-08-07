from app.script import script, scriptService
from main import constants
from app.summary import summary
from app.quiz import quiz


class ResponseModel:
    def __init__(self):
        self.video_id = ''
        self.summary = ''
        self.quizzes = []

    def setResponse(self, video_id: str, summary: str, quizzes: list):
        self.video_id = video_id
        self.summary = summary
        self.quizzes = quizzes


async def index(video_id: str = '', lang: str = constants['default_language']):
    youtube_script = script.Script()
    response = ResponseModel()
    scriptService.get_script(youtube_script, video_id, lang)

    response.video_id = video_id
    response.summary = summary.generate_summary(youtube_script.text)
    response.quizzes = quiz.generate_quiz(response.summary)

    return response
