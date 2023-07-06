import tiktoken
from fastapi import FastAPI
from youtube_transcript_api import YouTubeTranscriptApi
import os
import openai

app = FastAPI()

DEFAULT_LANGUAGE = 'ko'
openai.api_key = os.environ["GPT_API_KEY"]


@app.get("/")
async def root(video_id: str = '', lang: str = DEFAULT_LANGUAGE):
    youtube_script = Script()
    youtube_script.get_script(video_id, lang)
    return youtube_script.text, youtube_script.token_count


@app.get("/gpt")
async def gpt(input: str):
    gpt_model = Gpt()
    return gpt_model.request_gpt(input)


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

    def request_gpt(self, input):
        self.input = input
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a assistant"},
                {"role": "user", "content": self.input}
            ]
        )
        self.output = response["choices"][0]["message"]["content"]
        return self.output
