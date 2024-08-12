from youtube_transcript_api import YouTubeTranscriptApi
import tiktoken

from app.script.script import *
from main import constants


def get_script(script: Script, video_id: str):
    available_language = ''

    try:
        lang_list = YouTubeTranscriptApi.list_transcripts(video_id)
    except Exception as e:
        print(e)
        script.is_valid = False
        return

    for transcript in lang_list:
        if not transcript.is_generated:
            if transcript.language_code == 'ko':
                available_language = transcript
                break
            elif transcript.language_code == 'en':
                available_language = transcript
            elif available_language == '':
                available_language = transcript
        else:
            if not type(available_language) == str:
                break
            if transcript.language_code == 'ko':
                available_language = transcript
                break
            elif transcript.language_code == 'en':
                available_language = transcript
            elif available_language == '':
                available_language = transcript

    script.raw_script = available_language.fetch()
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
