from fastapi import FastAPI

# /api/app 에 마운트될 FastAPI 앱
app = FastAPI()  # 기본값: /docs, /openapi.json 제공

@app.get("/")
def root():
    return {"status": "ok", "hint": "GET /api/app/docs, GET /api/app/openapi.json"}
