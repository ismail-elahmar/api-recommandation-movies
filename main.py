from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

from ml_manager import ModelManager
from services import RecommendationService


@asynccontextmanager
async def lifespan(app: FastAPI):
    mgr = ModelManager()         
    mgr.load("similarity_df.pkl") 
    mgr.wait_until_ready(timeout=60)

    app.state.svc = RecommendationService(mgr)
    print("[Lifespan] Application prête.")
    yield
    app.state.svc._executor.shutdown(wait=False)
    print("[Lifespan] Application arrêtée.")


run = FastAPI(lifespan=lifespan)


@run.get("/", response_class=HTMLResponse, include_in_schema=False)
async def ui():
    return open(Path(__file__).parent / "ui.html", encoding="utf-8").read()


@run.get("/recommend/")
async def recommend(
    movie_name: str = Query(...),
    limit: int = Query(10, ge=1, le=50),
):
    svc: RecommendationService = run.state.svc
    result = await svc.recommend(movie_name=movie_name, limit=limit)
    return result.to_dict()


@run.get("/search/")
async def search(
    q: str = Query(...),
    max_results: int = Query(20, ge=1, le=100),
):
    svc: RecommendationService = run.state.svc
    results = await svc.search(q, max_results)
    return {"query": q, "results": results}


@run.get("/stats/")
async def stats():
    svc: RecommendationService = run.state.svc
    return svc.stats()
