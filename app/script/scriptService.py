from youtube_transcript_api import YouTubeTranscriptApi
import tiktoken

from app.script.script import *
from main import constants


def get_script(script: Script, video_id: str, lang: str):
    script.raw_script = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
    script.text = parse_script(script.raw_script)
    script.token_count = count_token(script.text)


def parse_script(raw_script: dict):
    text = ''
    for i in range(len(raw_script)):
        text += raw_script[i]['text'] + ' '

    return text


def count_token(text: str):
    tokenizer = tiktoken.encoding_for_model(constants['gpt_model']['small'])

    tokens = tokenizer.encode(text)
    token_count = len(tokens)

    return token_count
