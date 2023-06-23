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

3. FastAPI 설치하기
   
   우선 본 레포지토리를 클론하고 터미널의 현재 경로를 해당 레포지토리로 이동시킨다.

   ```bash
   pip3 install fastapi
   pip3 install uvicorn
   ```
   를 입력하여 해당 라이브러리를 설치한다.

   설치 후

   ```bash
   python3 -m uvicorn main:app --reload
   ```
   를 입력하면 localhost:8000 url 이 뜬다. 해당 페이지에 접속하여

   {"message" : "welcome to sroom ai"} 라고 뜨면 개발 세팅 끝!
   
