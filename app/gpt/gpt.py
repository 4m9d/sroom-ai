import openai
import os

from main import constants
from app.script.script import *


openai.api_key = os.environ['GPT_API_KEY']


def request_gpt(prompt: str):
    response = openai.ChatCompletion.create(
        model=constants['gpt_model']['4k'],
        messages=[
            constants['prompt']['system_message'],
            {"role": "user", "content": prompt}
        ],
        temperature=constants['model_parameter']['temperature']['high'],
        max_tokens=constants['model_parameter']['max_token']['1k']
    )

    return response["choices"][0]["message"]["content"]


def generate_summary(script: Script):
    summary_prompt = constants['prompt']['summary']
    prompt = script.text + summary_prompt

    summary = request_gpt(prompt)
    summary = summary.replace("\n", "\\n")
    summary = summary.replace("\"", "\\\"")

    return summary


def generate_quiz(summary: str):
    quiz_prompt = constants['prompt']['quiz']

    prompt = summary + quiz_prompt

    quiz_json = ''
    quiz_json += request_gpt(prompt)
    quiz_json = quiz_json.replace("\n", "")
    quiz_json = quiz_json.replace("\"", '"')

    quiz_json = quiz_json[1:-1]

    return quiz_json
