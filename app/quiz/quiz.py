from app.gpt.gpt import *
from main import constants


def generate_quiz(summary: str):
    
    quiz_prompt = constants['prompt']['quiz']
    prompt = summary + quiz_prompt

    gpt_response = request_gpt(prompt)

    quiz_json = reformat_quiz(gpt_response)

    return quiz_json


def reformat_quiz(quiz_json: str):
    quiz_json = quiz_json.replace("\n", "")
    quiz_json = quiz_json.replace("\"", '"')

    quiz_json = quiz_json[1:-1]

    return quiz_json
