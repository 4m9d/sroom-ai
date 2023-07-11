import tiktoken
from fastapi import FastAPI
from youtube_transcript_api import YouTubeTranscriptApi
import os
import openai
import json
import yaml

app = FastAPI()

with open('constants.yaml', encoding='UTF-8') as f:
    constants = yaml.load(f, Loader=yaml.FullLoader)

openai.api_key = os.environ['GPT_API_KEY']

@app.get("/")
async def root(video_id: str = '', lang: str = constants['default_language']):
    youtube_script = Script()
    youtube_script.get_script(video_id, lang)
    gpt = Gpt()

    # 스크립트가 3000토큰이 넘을 경우 요약본 생성이 현 시점에선 불가능 하므로 에러 메시지와 함께 리턴
    if youtube_script.token_count > constants['script']['max_token']:
        return "Error : " + constants['message']['error']['over_token']

    # GPT로부터 요약본 생성
    summary = gpt.generate_summary(youtube_script)

    # 생성한 요약본을 기준으로 GPT로부터 퀴즈 생성
    quiz = gpt.generate_quiz(summary)

    # GPT로 부터 받은 여러 정보들을 JSON 양식에 맞게 조합
    response_string = '{'
    response_string += '"videoCode": "{0}", "summary": "{1}", {2}'.format(video_id, summary, quiz)
    response_string += '}'

    # 조합한 String을 JSON 형식으로 변환
    response_json = json.loads(response_string)

    return response_json


class Script:
    def __init__(self):
        self.raw_script = ''
        self.text = ''
        self.token_count = 0

    def get_script(self, video_id: str, lang: str):
        self.raw_script = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
        self.to_text(self.raw_script)
        self.count_token(self.text)

    def to_text(self, raw_script: dict):
        for i in range(len(raw_script)):
            self.text += raw_script[i]['text'] + ' '

    def count_token(self, text: str):
        tokenizer = tiktoken.encoding_for_model(constants['gpt_model']['4k'])

        tokens = tokenizer.encode(text)
        self.token_count = len(tokens)


class Gpt:
    def __init__(self):
        self.input = ''
        self.output = ''

    def request_gpt(self, prompt: str):
        self.input = prompt
        response = openai.ChatCompletion.create(
            model=constants['gpt_model']['4k'],
            messages=[
                constants['prompt']['system_message'],
                {"role": "user", "content": self.input}
            ],
            temperature=constants['model_parameter']['temperature']['high'],
            max_tokens=constants['model_parameter']['max_token']['1k']
        )
        self.output = response["choices"][0]["message"]["content"]
        return self.output

    def generate_summary(self, script: Script):

        summary_prompt = constants['prompt']['summary']
        prompt = script.text + summary_prompt

        summary = self.request_gpt(prompt)
        summary = summary.replace("\n", "\\n")
        summary = summary.replace("\"", "\\\"")

        return summary

    def generate_quiz(self, summary: str):
        quiz_prompt = constants['prompt']['quiz']

        prompt = summary + quiz_prompt

        quiz_json = ''
        quiz_json += self.request_gpt(prompt)
        quiz_json = quiz_json.replace("\n", "")
        quiz_json = quiz_json.replace("\"", '"')

        quiz_json = quiz_json[1:-1]

        return quiz_json
