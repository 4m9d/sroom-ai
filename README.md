## sroom-ai

welcome to sroom ai

## 필독! Sroom AI Server 환경 세팅

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
 
4. Celery 환경 세팅 

   앞서 pip3 install 명령어를 통해 celery 라이브러리 설치는 완료되었으나 메시지 블로커와 결과 백엔드를 위한
   DB 설치가 필요하다

   ```bash
   brew install redis
   ```

   를 통해 redis를 설치한다.

5. 실행하기

   모든 세팅이 완료되었다면 아래 명령어를 통해 실행해야 한다.
   brew 명령어를 제외한 모든 명령은 프로젝트 패키지 안에서 실행해야 한다.
   또한 각 명령어를 서로 다른 터미널에서 실행해야 한다.

   ```bash
   brew services start redis
   celery -A celery_app worker -l info
   celery -A celery_app flower --address=localhost --port=5555
   python3 main.py local
   ```

   모든 명령어를 입력해 정상 동작이 확인되면 아래 URL 및 API를 통해 작동 시킬 수 있다.


   ```bash
   http://127.0.0.1:8000/?video_id={}
   ```
   해당 Url에서 유튜브 video_id를 넣으면 작업이 등록되며

   ```bash
   http://127.0.0.1:5555
   ```
   를 통해 등록된 작업 목록을 확인할 수 있다.

   ```bash
   http://127.0.0.1:8000/results
   ```
   에서는 아직 조회하지 않은 모든 작업 수행 결과가 리스트 형태로 반환된다.
