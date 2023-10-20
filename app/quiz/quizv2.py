import json


from main import constants
from app.gpt import gpt

MAX_TRY_COUNT = 3


async def generate_quizzes(summary: str):
    prompt = summary + constants['prompt']['multiple_choice_quiz']['kr']
    quiz_json = {}
    system_message = constants['prompt']['multiple_choice_quiz']['system_message']

    for count in range(MAX_TRY_COUNT):
        gpt_response = await gpt.request_gpt(prompt, system_message)
        quiz_json, is_valid = _reformat_quiz(gpt_response)
        if is_valid:
            break

    return quiz_json


def _reformat_quiz(quiz_json: str):
    quiz_json = quiz_json.replace("\n", "")
    quiz_json = quiz_json.replace("\"", '"')

    try:
        quiz_json = json.loads(quiz_json)
    except json.decoder.JSONDecodeError as e:
        print("JSON Decode Error : retry generate quiz")
        return [{'quiz_type': 2, 'quiz_question': '퀴즈 생성중 오류가 발생했습니다. ㅠㅠ', 'quiz_select_options': [], 'answer': ''}], False

    return quiz_json, True
