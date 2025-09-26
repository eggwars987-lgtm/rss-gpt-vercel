from fastapi import FastAPI

# /api/app 아래에 문서/헬스/런 엔드포인트 명시
app = FastAPI(
    title="rss-gpt-vercel",
    docs_url="/docs",           # Swagger UI -> /api/app/docs
    redoc_url=None,
    openapi_url="/openapi.json" # OpenAPI JSON -> /api/app/openapi.json
)

@app.get("/")
def root():
    return {
        "status": "ok",
        "hint": "GET /api/app/docs, GET /api/app/health, POST /api/app/run"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

# 임시 실행 엔드포인트(나중에 실제 로직 넣으면 됨)
@app.post("/run")
def run():
    return {"ok": True}
