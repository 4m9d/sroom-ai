import openai
import os

from main import constants
from app.script.script import *


openai.api_key = os.environ['GPT_API_KEY']


def request_gpt(prompt: str):
    response = openai.ChatCompletion.create(
        model=constants['gpt_model']['small'],
        messages=[
            constants['prompt']['system_message'],
            {"role": "user", "content": prompt}
        ],
        temperature=constants['model_parameter']['temperature']['high'],
        max_tokens=constants['model_parameter']['max_token']['1k']
    )

    return response["choices"][0]["message"]["content"]
