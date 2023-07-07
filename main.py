import tiktoken
from fastapi import FastAPI
from youtube_transcript_api import YouTubeTranscriptApi
import os
import openai

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
    summary = gpt.generate_summary(youtube_script)
    return summary

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

        return self.request_gpt(prompt)