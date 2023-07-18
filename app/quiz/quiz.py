from app.gpt.gpt import *
from main import constants
import json

def generate_quiz(summary: str):
    
    quiz_prompt = constants['prompt']['quiz']
    prompt = summary + quiz_prompt

    gpt_response = request_gpt(prompt)

    quiz_json = reformat_quiz(gpt_response)

    quizes = []
    for quiz in quiz_json['quizes']:
        quizes.append(quiz)

    return quizes


def reformat_quiz(quiz_json: str):
    quiz_json = quiz_json.replace("\n", "")
    quiz_json = quiz_json.replace("\"", '"')

    quiz_json = json.loads(quiz_json)

    return quiz_json
