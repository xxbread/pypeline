
from datetime import datetime
from threading import Lock
from typing import Literal

class Log:

    _lock = Lock()
    _colors = {
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'purple': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'grey': '\033[90m',
        'reset': '\033[0m',
    }

    @classmethod
    def _color(cls, text: str, color: str) -> str:
        return f"{cls._colors[color]}{text}{cls._colors['reset']}"

    @classmethod
    def _timestamp(cls) -> str:
        return f"{cls._color(datetime.now().strftime('[%H:%M:%S]'), 'cyan')}"

    @classmethod
    def send(cls, text: str, color: Literal['red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white', 'grey'] = "white") -> None:
        with cls._lock:
            print(f"{cls._timestamp()} {cls._color('>', 'cyan')} {cls._color(text, color)}")
        
    @classmethod
    def ask(cls) -> str:
        with cls._lock:
            return input(f"{cls._timestamp()} {cls._color(' >> ', 'cyan')}")