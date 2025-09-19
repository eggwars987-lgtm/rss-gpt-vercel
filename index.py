# Vercel serverless Python → FastAPI 호환 핸들러
# 최소 기능: Google News RSS(ko-KR)에서 카테고리 기사 수집 → 간단 요약/클러스터링 흉내 → JSON 반환

import os
from datetime import datetime
import feedparser
from dateutil import tz
from fastapi import FastAPI
from pydantic import BaseModel
import re

KST = tz.gettz("Asia/Seoul")
DEFAULT_LIMIT = int(os.getenv("DEFAULT_LIMIT_PER_FEED", "12"))
ESSAY_MAX = int(os.getenv("ESSAY_MAX_CHARS", "200"))

app = FastAPI()

class RunReq(BaseModel):
    limit_per_feed: int = DEFAULT_LIMIT
    essay_max_chars: int = ESSAY_MAX

FEEDS = {
    "policy": "https://news.google.com/rss/search?q=%EC%A0%95%EC%B1%85+OR+%EA%B5%AD%ED%9A%8C+OR+%EB%B3%B4%EA%B1%B4%EB%B3%B5%EC%A7%80%EB%B6%80&hl=ko&gl=KR&ceid=KR:ko",
    "welfare": "https://news.google.com/rss/search?q=%EB%B3%B5%EC%A7%80+OR+%EC%97%B0%EA%B8%88+OR+%EC%9A%B4%EC%98%81%EB%B3%B4%EC%A1%B0&hl=ko&gl=KR&ceid=KR:ko",
    "finance": "https://news.google.com/rss/search?q=%EA%B8%88%EC%9C%B5+OR+%EA%B8%88%EB%A6%AC+OR+%EA%B8%88%EA%B0%90%EC%9B%90&hl=ko&gl=KR&ceid=KR:ko",
    "equity": "https://news.google.com/rss/search?q=%EC%A6%9D%EC%8B%9C+OR+%EC%BD%94%EC%8A%A4%ED%94%BC+OR+%EC%BD%94%EC%8A%A4%EB%8B%A5&hl=ko&gl=KR&ceid=KR:ko"
}

def normalize_title(t: str) -> str:
    t = re.sub(r"\[[^\]]+\]", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

@app.post("/run")
async def run(req: RunReq):
    items = []
    for cat, url in FEEDS.items():
        d = feedparser.parse(url)
        for e in d.entries[: req.limit_per_feed]:
            title = normalize_title(getattr(e, "title", ""))
            link = getattr(e, "link", "")
            items.append({"cat": cat, "title": title, "link": link})

    out_clusters = []
    for cat in ["policy","welfare","finance","equity"]:
        arr = [x for x in items if x["cat"] == cat][:3]
        if not arr:
            continue
        topic = {
            "policy": "시사·정책",
            "welfare": "복지",
            "finance": "금융",
            "equity": "주식/증시"
        }[cat]
        key_points = [x["title"] for x in arr]
        sources = [x["link"] for x in arr]
        insights = {"so_what": [f"{topic} 이슈 점검"], "watchlist": [f"{topic} 후속 보도"]}
        out_clusters.append({"topic": topic, "key_points": key_points, "insights": insights, "sources": sources})

    now = datetime.now(KST).strftime("%Y-%m-%d %H:%M KST")
    essay = "헤드라인은 바뀐다. 오늘의 기준을 내일 다시 점검하라. 흐름을 잡는 쪽이 리스크를 줄인다."
    if len(essay) > req.essay_max_chars:
        essay = essay[: req.essay_max_chars]

    return {"generated_at": now, "clusters": out_clusters, "essays": [{"text": essay}]}
