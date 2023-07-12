from youtube_transcript_api import YouTubeTranscriptApi
from app.script.script import *
import tiktoken


from main import constants


def get_script(script: Script, video_id: str, lang: str):
    script.raw_script = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
    script.text = to_text(script.raw_script)
    script.token_count = count_token(script.text)


def to_text(raw_script: dict):
    text = ''
    for i in range(len(raw_script)):
        text += raw_script[i]['text'] + ' '

    return text


def count_token(text: str):
    tokenizer = tiktoken.encoding_for_model(constants['gpt_model']['4k'])

    tokens = tokenizer.encode(text)
    token_count = len(tokens)

    return token_count
