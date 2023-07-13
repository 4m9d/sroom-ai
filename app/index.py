from app.script.scriptService import *
from main import constants
from app.gpt.gpt import *
import json


async def index(video_id: str = '', lang: str = constants['default_language']):
    youtube_script = Script()
    get_script(youtube_script, video_id, lang)

    # 스크립트가 3000토큰이 넘을 경우 요약본 생성이 현 시점에선 불가능 하므로 에러 메시지와 함께 리턴
    if youtube_script.token_count > constants['script']['max_token']:
        return "Error : " + constants['message']['error']['over_token']

    # GPT로부터 요약본 생성
    summary = generate_summary(youtube_script)

    # 생성한 요약본을 기준으로 GPT로부터 퀴즈 생성
    quiz = generate_quiz(summary)

    # GPT로 부터 받은 여러 정보들을 JSON 양식에 맞게 조합

    response = jsonify_response(video_id, summary, quiz)

    return response


def jsonify_response(video_id: str, summary: str, quiz: str):
    response_string = '{'
    response_string += '"videoCode": "{0}", "summary": "{1}", {2}'.format(video_id, summary, quiz)
    response_string += '}'

    # 조합한 String을 JSON 형식으로 변환
    response_json = json.loads(response_string)

    return response_json
