from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class RecommendationResult:
    movie: str
    recommendations: list[str]

    def to_dict(self):
        return {
            "movie": self.movie,
            "recommendations": self.recommendations,
        }


@dataclass
class ModelInfo:
    path: Path
    loaded: bool
    shape: Optional[tuple] = None
