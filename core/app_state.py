import logging
from threading import Lock
from types import SimpleNamespace
from core.config_manager import config_read, config_dump
from typing import Callable, List, Any, Dict


logger = logging.getLogger(__name__)
class Config:
    _instance = None
    _observers: List[Callable[[], None]] = []
    _initialized = False
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        logger.debug("Initializing Config singleton")
        self._initialized = True
        self.load()

    def load(self):
        '''Loading configuration data from ./config.yaml'''
        logger.info("Loading configuration from ./config.yaml")
        cfg = config_read()
        self.data = dict2ns(cfg)
        self._notify()

    def save(self):
        '''Save current configuration data to ./config.yaml'''
        logger.info("Saving configuration to ./config.yaml")
        cfg = ns2dict(self.data)
        config_dump(cfg)

    def _notify(self):
        for cb in self._observers:
            cb()

    def register(self, callback: Callable[[], None]):
        '''Register a callback to be called on config change'''
        logger.debug("Registering config observer: %s", callback)
        self._observers.append(callback)

    def __getattr__(self, item: str):
        return getattr(self.data, item)

    def __setattr__(self, key: str, value: Any):
        if key in ("_instance", "_observers", "data"):
            super().__setattr__(key, value)
        else:
            logger.debug("Updating config: %s = %s", key, value)
            setattr(self.data, key, value)
            self._notify()

def dict2ns(d: dict[str, Any]) -> SimpleNamespace:
    '''Convert dict to SimpleNamespace recursively'''
    return SimpleNamespace(**{k: dict2ns(v) for k, v in d.items()})

def ns2dict(ns: SimpleNamespace) -> Dict[str, Any]:
    """Convert SimpleNamespace to dict recursively"""
    return {k: ns2dict(v) for k, v in vars(ns).items()}


config = Config()

