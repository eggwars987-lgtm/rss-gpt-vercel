from fastapi import FastAPI

# Vercel 함수 경로에 맞춰 루트패스/문서 경로 고정
app = FastAPI(
    title="rss-gpt-vercel",
    root_path="/api/app",                   # ★ 핵심
    docs_url="/api/app/docs",               # Swagger UI
    redoc_url=None,
    openapi_url="/api/app/openapi.json"     # OpenAPI JSON
)

@app.get("/")
def root():
    return {
        "status": "ok",
        "hint": "GET /api/app/docs, GET /api/app/health, POST /api/app/run"
    }

@app.get("/health")
def health():
    return {"ok": True}
