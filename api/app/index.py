# /api/app/index.py
from fastapi import FastAPI

# Vercel에서 이 함수는 /api/app 아래로 마운트됩니다.
# 그래서 root_path="/api/app" 를 지정해야 /docs, /openapi.json 이 올바른 경로로 붙습니다.
app = FastAPI(
    title="rss-gpt-vercel",
    root_path="/api/app",
    docs_url="/docs",           # Swagger UI ->  /api/app/docs
    redoc_url=None,             # (원하면 "/redoc"으로 따로 켤 수 있어요)
    openapi_url="/openapi.json" # OpenAPI JSON -> /api/app/openapi.json
)

@app.get("/")
def root():
    return {"status": "ok", "hint": "GET /api/app/docs, GET /api/app/health, POST /api/app/run"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run")
def run():
    # 최소 동작 확인용
    return {"ok": True}
