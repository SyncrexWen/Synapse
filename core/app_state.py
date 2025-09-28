from threading import Lock
from types import SimpleNamespace
from core.config_manager import config_read, config_dump


class Config:
    _instance = None
    _observers = []
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
        self.load()

    def load(self):
        '''Loading configuration data from ./config.yaml'''
        cfg = config_read()
        self.data = dict2ns(cfg)
        self._notify()

    def save(self):
        '''Save current configuration data to ./config.yaml'''
        cfg = ns2dict(self.data)
        config_dump(cfg)

    def _notify(self):
        for cb in self._observers:
            cb()

    def register(self, callback):
        '''Register a callback to be called on config change'''
        self._observers.append(callback)

    def __getattr__(self, item):
        return getattr(self.data, item)

    def __setattr__(self, key, value):
        if key in ("_instance", "_observers", "data"):
            super().__setattr__(key, value)
        else:
            setattr(self.data, key, value)
            self._notify()

def dict2ns(d: dict) -> SimpleNamespace:
    '''Convert dict to SimpleNamespace recursively'''
    if isinstance(d, dict):
        return SimpleNamespace(**{k: dict2ns(v) for k, v in d.items()})
    elif isinstance(d, list):
        return [dict2ns(i) for i in d]
    else:
        return d

def ns2dict(ns):
    """Convert SimpleNamespace to dict recursively"""
    if isinstance(ns, SimpleNamespace):
        return {k: ns2dict(v) for k, v in vars(ns).items()}
    elif isinstance(ns, list):
        return [ns2dict(item) for item in ns]
    elif isinstance(ns, dict):
        return {k: ns2dict(v) for k, v in ns.items()}
    else:
        return ns


config = Config()

