import pickle
import threading
from pathlib import Path

from interfaces import IModelRepository
from schemas import ModelInfo


class ModelManager(IModelRepository):
   

    _instance = None
    _lock = threading.Lock()          
    _load_lock = threading.Lock()     
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._df = None
                cls._instance._ready = threading.Event()
                cls._instance._info: ModelInfo | None = None
        return cls._instance
    def load(self, path: str = "similarity_df.pkl") -> ModelInfo:
       
        p = Path(path)
        self._info = ModelInfo(path=p, loaded=False)
        self._ready.clear()

        thread = threading.Thread(
            target=self._load_worker,
            args=(p,),
            daemon=True,         
            name="ModelLoader",
        )
        thread.start()
        return self._info

    def _load_worker(self, p: Path) -> None:
        try:
            with open(p, "rb") as f:
                data = pickle.load(f)
            with self._load_lock:
                self._df = data
                self._info.loaded = True
                self._info.shape = data.shape
            print(f"[ModelLoader] Modèle chargé : {data.shape}")
        except FileNotFoundError:
            print(f"[ModelLoader] Erreur : fichier introuvable → {p}")
        finally:
            self._ready.set()     
    def wait_until_ready(self, timeout: float = 30.0) -> bool:
        """Bloque jusqu'à ce que le chargement soit terminé (ou timeout)."""
        return self._ready.wait(timeout=timeout)

    @property
    def is_loaded(self) -> bool:
        with self._load_lock:
            return self._df is not None

    @property
    def movies(self) -> list[str]:
        with self._load_lock:
            return self._df.columns.tolist() if self._df is not None else []

    @property
    def df(self):
        with self._load_lock:
            return self._df
