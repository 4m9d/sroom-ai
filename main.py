from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message" : "welcome to sro``om ai server"}