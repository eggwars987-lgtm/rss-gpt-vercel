# api/app/index.py
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="rss-gpt-vercel")

class RunReq(BaseModel):
    limit_per_feed: int = 12
    essay_max_chars: int = 200

@app.get("/")
def root():
    # 루트 헬스(지금 OK가 뜨는 곳)
    return {"status": "ok", "hint": "GET /api/app/health, POST /api/app/run"}

@app.get("/health")
def health():
    return {"status": "ok", "route": "/api/app"}

@app.post("/run")
def run(req: RunReq):
    # 실제 RSS 파이프라인은 나중에 붙이고, 일단 형식만 맞춰 더미 응답
    now_kst = (datetime.now(timezone.utc) + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M KST")
    return {
        "generated_at": now_kst,
        "clusters": [
            {
                "topic": "시사·정책",
                "key_points": ["핵심 포인트 1", "핵심 포인트 2"],
                "insights": ["요지는 이렇다...", "시장에 미치는 영향은..."],
                "essays": [
                    {"text": "요즘 뉴스 흐름을 보면 ... (샘플 에세이)", "source_count": 3}
                ],
            }
        ],
    }
