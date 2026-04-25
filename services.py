import asyncio
from concurrent.futures import ProcessPoolExecutor
from fastapi import HTTPException

from interfaces import IModelRepository, IRecommendationService
from schemas import RecommendationResult
from utils import log_call, positive


def _compute_scores(records: list[tuple[str, float]], limit: int) -> list[str]:
   
    sorted_recs = sorted(records, key=lambda x: x[1], reverse=True)
    return [title for title, _ in sorted_recs[:limit]]

class RecommendationService(IRecommendationService):

    def __init__(self, mgr: IModelRepository):
        self.m = mgr                              
        self._executor = ProcessPoolExecutor()    

    def _check(self, movie: str | None = None) -> None:
        if not self.m.is_loaded:
            raise HTTPException(503, "Model not loaded")
        if movie and movie not in self.m.df.columns:
            raise HTTPException(404, f"Movie not found: {movie}")

    @log_call
    @positive("limit")
    async def recommend(self, movie_name: str, limit: int = 10) -> RecommendationResult:
      
        self._check(movie_name)

        series = self.m.df[movie_name].drop(index=movie_name, errors="ignore")
        records: list[tuple[str, float]] = list(series.items())

        loop = asyncio.get_event_loop()
        top_movies: list[str] = await loop.run_in_executor(
            self._executor,
            _compute_scores,
            records,
            limit,
        )

        return RecommendationResult(movie=movie_name, recommendations=top_movies)

    async def search(self, q: str, n: int = 20) -> list[str]:
       
        results = []
        for movie in self.m.movies:
            if q.lower() in movie.lower():
                results.append(movie)
                if len(results) >= n:
                    break
            await asyncio.sleep(0)   
        return results

    def stats(self) -> dict:
        if self.m.is_loaded:
            return {"loaded": True, "total_movies": len(self.m.movies)}
        return {"loaded": False}
