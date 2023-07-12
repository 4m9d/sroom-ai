## sroom-ai

welcome to sroom ai


## 필독! FastAPI 개발환경 세팅

1. 파이썬 설치하기
   
   [파이썬 설치 링크](https://www.python.org/downloads/)

   이 링크 타고 가서 3.11.4 버전을 다운 받는다.

   설치 하고 나서 터미널에서
   ```bash
   python3 --version
   ```
   를 입력했을 때 3.11.4 라는 출력이 나오면 정상적으로 설치 된 것!

   간혹 분명 설치했는데 Not Found 라고 뜰 수 있다.
   이는 환경변수가 세팅되지 않은 것으로

   ```bash
   echo "alias python=/usr/bin/python3" >> ~/.zshrc
   source ~/.zshrc
   ```
   를 통해 환경변수를 세팅하자

3. FastAPI 설치하기
   
   우선 본 레포지토리를 클론하고 터미널의 현재 경로를 해당 레포지토리로 이동시킨다.

   ```bash
   pip3 install -r requirements.txt
   ```
   를 입력하여 요구되는 패키지 들을 자동으로 설치한다.

   환경변수 "GPT_API_KEY"를 생성하여 본인의 API키를 저장한다.

   ```bash
   python3 main.py
   ```
   를 입력하면 localhost:8000 url 이 뜬다. 해당 페이지에 접속하면

   처음에는 "Internal Server Error"라고 뜬다.

   여기에 "/?video_id={EXAMPLE_ID}&lang={AUDIO_LANGUAGE}" 를 추가하여 실행하면
   요약본, 퀴즈가 담긴 JSON이 리턴된다.
   