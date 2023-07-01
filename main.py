from fastapi import FastAPI
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI()

DEFAULT_LANGUAGE = 'ko'
@app.get("/")
async def root(video_id: str = '', lang: str = DEFAULT_LANGUAGE):
    youtube_script = Script()
    youtube_script.get_script(video_id, lang)
    return youtube_script.text


class Script:
    def __init__(self):
        self.raw_script = ''
        self.text = ''

    def get_script(self, video_id, lang):
        self.raw_script = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
        self.to_text(self.raw_script)

    def to_text(self, raw_script):
        for i in range(len(raw_script)):
            self.text += raw_script[i]['text'] + ' '
