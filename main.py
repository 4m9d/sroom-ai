import tiktoken
from fastapi import FastAPI
from youtube_transcript_api import YouTubeTranscriptApi
import os
import openai
import json

app = FastAPI()

DEFAULT_LANGUAGE = 'ko'
GPT_MODEL = 'gpt-3.5-turbo'
openai.api_key = os.environ["GPT_API_KEY"]
MODEL_PARAMETERS = {
    "temperatures_high": 0.7,
    "temperatures_low": 0.3,
    "max_token_1000": 1000
}


@app.get("/")
async def root(video_id: str = '', lang: str = DEFAULT_LANGUAGE):
    youtube_script = Script()
    youtube_script.get_script(video_id, lang)
    gpt = Gpt()

    # 스크립트가 3000토큰이 넘을 경우 요약본 생성이 현 시점에선 불가능 하므로 에러 메시지와 함께 리턴
    if youtube_script.token_count > 3000:
        return "Over Token"

    # GPT로부터 요약본 생성
    summary = gpt.generate_summary(youtube_script)

    # 생성한 요약본을 기준으로 GPT로부터 퀴즈 생성
    quiz = gpt.generate_quiz(summary)

    # GPT로 부터 받은 여러 정보들을 JSON 양식에 맞게 조합
    response_string = ''

    response_string += '{"videoCode": "' + video_id + '", '
    response_string += '"summary": "' + summary + '", '
    response_string += quiz + '}'

    # 조합한 String을 JSON 형식으로 변환
    response_json = json.loads(response_string)

    return response_json


class Script:
    def __init__(self):
        self.raw_script = ''
        self.text = ''
        self.token_count = 0

    def get_script(self, video_id, lang):
        self.raw_script = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
        self.to_text(self.raw_script)
        self.count_token(self.text)

    def to_text(self, raw_script):
        for i in range(len(raw_script)):
            self.text += raw_script[i]['text'] + ' '

    def count_token(self, text):
        tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")

        tokens = tokenizer.encode(text)
        self.token_count = len(tokens)


class Gpt:
    def __init__(self):
        self.input = ''
        self.output = ''

    def request_gpt(self, prompt):
        self.input = prompt
        response = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "You are an assistant that generates quizzes and summaries"},
                {"role": "user", "content": self.input}
            ],
            temperature=MODEL_PARAMETERS["temperatures_high"],
            max_tokens=MODEL_PARAMETERS["max_token_1000"]
        )
        self.output = response["choices"][0]["message"]["content"]
        return self.output

    def generate_summary(self, script):
        if script.token_count > 3000:
            return "Error : Over Token"

        summary_prompt = "\n\n 위 스크립트를 최대한 모든 내용이 반영될 수 있도록 요약해줘"
        prompt = script.text + summary_prompt

        summary = self.request_gpt(prompt)
        summary = summary.replace("\n", "\\n")
        summary = summary.replace("\"", "\\\"")

        return summary

    def generate_quiz(self, summary):
        quiz_prompt = "\n\n 위 요약본을 바탕으로 객관식 1문제, 주관식 1문제, True or False 1문제 내줘.\n" \
                      "JSON 형식으로 답변해주고 아래 형식을 지켜셔 답변해줘" \
                      "quizes: [{\"quizType\":\"\" , \"quizQuestion\":\"\", \"quizSelectOption1\": \"\", \"quizSelectOption2\": \"\", \"quizSelectOption3\": \"\", \"quizSelectOption4\": \"\", \"answer\":\"\"}]" \
                      "quiz_type은 객관식이면 1, 주관식이면 2, TF면 3으로 할당해주고 객관식 정답은 번호만 넣어줘" \
                      "주관식의 경우 quizSelectOption에는 전부 null 값을 넣어주고, TF 문제는 Option1 에 true, Option2 에 false를 넣어줘" \
                      "TF문제 정답은 true일 경우 1, false 일 경우 2로 반환해줘" \
                      "각 문제 중괄호 사이에 반드시 ,을 넣어줘"

        prompt = summary + quiz_prompt
        quiz_json = ''
        quiz_json += self.request_gpt(prompt)
        quiz_json = quiz_json.replace("\n", "")
        quiz_json = quiz_json.replace("\"", '"')

        quiz_json = quiz_json[1:-1]

        return quiz_json
