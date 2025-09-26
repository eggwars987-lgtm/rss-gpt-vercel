from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "hint": "GET /api/app/docs, GET /api/app/openapi.json"}
