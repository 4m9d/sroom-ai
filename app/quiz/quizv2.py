import asyncio
import json

from main import constants
from app.gpt import gpt

MAX_TRY_COUNT = 3


async def generate_quizzes(summaries: list):

    if len(summaries) == 1:
        quiz_count = 3
    else:
        quiz_count = 2

    tasks = [generate_quizzes_chunk(summary, quiz_count) for summary in summaries]
    quiz_chunk_list = await asyncio.gather(*tasks)

    quiz_list = []
    for quiz_chunk in quiz_chunk_list:
        quiz_list.extend(quiz_chunk)

    for quiz in quiz_list:
        if isinstance(quiz['answer'], list) and len(quiz['answer']) > 0:
            quiz['answer'] = quiz['answer'][0]

        if quiz['answer'] == 0:
            quiz['answer'] = 1

        if len(quiz['quiz_select_options']) < quiz['answer']:
            quiz['answer'] = len(quiz['quiz_select_options'])

    return quiz_list


async def generate_quizzes_chunk(summary: str, quiz_count: int):
    prompt = summary + constants['prompt']['multiple_choice_quiz']['kr'] + str(quiz_count)
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
        return [{'quiz_type': 1, 'quiz_question': 'ERROR!', 'quiz_select_options': ['퀴즈 생성중 오류가 발생했습니다. ㅠㅠ'], 'answer': 1}], False

    return quiz_json, True
