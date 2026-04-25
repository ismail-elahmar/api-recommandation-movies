from abc import ABC, abstractmethod
from schemas import RecommendationResult, ModelInfo


class IModelRepository(ABC):
    """Interface abstraite pour tout dépôt de modèle de similarité."""

    @abstractmethod
    def load(self, path: str) -> ModelInfo:
        """Charge le modèle depuis un fichier et retourne ses infos."""
        ...

    @property
    @abstractmethod
    def is_loaded(self) -> bool:
        """Indique si le modèle est prêt à l'emploi."""
        ...

    @property
    @abstractmethod
    def movies(self) -> list[str]:
        """Retourne la liste de tous les films connus."""
        ...

    @property
    @abstractmethod
    def df(self):
        """Accès brut au DataFrame de similarité."""
        ...

class IRecommendationService(ABC):
    """Interface abstraite pour tout service de recommandation."""

    @abstractmethod
    async def recommend(self, movie_name: str, limit: int) -> RecommendationResult:
        """Retourne les `limit` films les plus similaires à `movie_name`."""
        ...

    @abstractmethod
    async def search(self, q: str, n: int) -> list[str]:
        """Recherche des titres contenant `q` (insensible à la casse)."""
        ...

    @abstractmethod
    def stats(self) -> dict:
        """Statistiques sur le modèle chargé."""
        ...
