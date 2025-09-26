# api/app/index.py
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI
from pydantic import BaseModel

# 문서/스키마 경로를 명시(디폴트지만 혹시 몰라 확실히 적어둠)
app = FastAPI(
    title="rss-gpt-vercel",
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url="/redoc",
)

class RunReq(BaseModel):
    limit_per_feed: int = 12
    essay_max_chars: int = 200

@app.get("/")
def root():
    # 루트 확인용
    return {"status": "ok", "hint": "GET /api/app/health, POST /api/app/run"}

@app.get("/health")
def health():
    return {"status": "ok", "route": "/api/app"}

@app.post("/run")
def run(req: RunReq):
    now_kst = (datetime.now(timezone.utc) + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M KST")
    return {
        "generated_at": now_kst,
        "clusters": [
            {
                "topic": "시사·정책",
                "key_points": ["핵심 포인트 1", "핵심 포인트 2"],
                "insights": ["요지는 이렇다...", "시장에 미치는 영향은..."],
                "essays": [{"text": "요즘 뉴스 흐름을 보면 ... (샘플 에세이)"}],
            }
        ],
    }

# 디버깅용: 현재 라우트 목록을 보여줌
@app.get("/__routes")
def __routes():
    return [getattr(r, "path", str(r)) for r in app.routes]
