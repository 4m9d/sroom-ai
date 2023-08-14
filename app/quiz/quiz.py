from app.gpt import gpt
from main import constants
import json

MAX_TRY_COUNT = 3


async def generate_quiz(summary: str):
    
    quiz_prompt = constants['prompt']['quiz']
    prompt = summary + quiz_prompt
    quiz_json = {}

    for count in range(MAX_TRY_COUNT):
        gpt_response = await gpt.request_gpt(prompt)
        quiz_json, is_valid = _reformat_quiz(gpt_response)
        if is_valid:
            break

    quizzes = []
    for quiz in quiz_json['quizzes']:
        quizzes.append(quiz)

    return quizzes


def _reformat_quiz(quiz_json: str):
    quiz_json = quiz_json.replace("\n", "")
    quiz_json = quiz_json.replace("\"", '"')

    try:
        quiz_json = json.loads(quiz_json)
    except json.decoder.JSONDecodeError as e:
        print("JSON Decode Error : retry generate quiz")
        return {'quizzes': []}, False

    return quiz_json, True
