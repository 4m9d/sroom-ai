import json

from main import constants
from app.gpt import gpt

MAX_TRY_COUNT = 3


async def generate_quizzes(summary: str, script_tokens: int):
    quiz_count = set_quiz_count(script_tokens)
    prompt = summary + constants['prompt']['multiple_choice_quiz']['kr'] + str(quiz_count)
    quiz_json = {}
    system_message = constants['prompt']['multiple_choice_quiz']['system_message']

    for count in range(MAX_TRY_COUNT):
        gpt_response = await gpt.request_gpt(prompt, system_message)
        quiz_json, is_valid = _reformat_quiz(gpt_response)
        if is_valid:
            break

    return quiz_json


def set_quiz_count(script_tokens: int):
    quiz_count = 3
    if script_tokens > 5000:
        quiz_count += int((script_tokens - 5000) / 2500) + 1
        if quiz_count > 15:
            quiz_count = 15

    return quiz_count


def _reformat_quiz(quiz_json: str):
    quiz_json = quiz_json.replace("\n", "")
    quiz_json = quiz_json.replace("\"", '"')

    try:
        quiz_json = json.loads(quiz_json)
    except json.decoder.JSONDecodeError as e:
        print("JSON Decode Error : retry generate quiz")
        return [{'quiz_type': 1, 'quiz_question': 'ERROR!', 'quiz_select_options': ['퀴즈 생성중 오류가 발생했습니다. ㅠㅠ'], 'answer': 1}], False

    return quiz_json, True
