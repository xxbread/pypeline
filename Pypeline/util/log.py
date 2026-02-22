
import os
from datetime import datetime
from threading import Lock
from typing import Literal
from contextlib import nullcontext

class Log:

    threaded = False
    _lock = Lock() if threaded else nullcontext()

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

    DefaultColor = "cyan"
    ColorOption = Literal['red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white', 'grey']

    @classmethod
    def _color(cls, text: str, color: str) -> str:
        return f"{cls._colors[color]}{text}{cls._colors['reset']}"

    @classmethod
    def _timestamp(cls, color: ColorOption) -> str:
        return f"{cls._color(datetime.now().strftime('[%H:%M:%S]'), color)}"

    @classmethod
    def _print(cls, text: str, color: ColorOption, nl: bool = False) -> None:
        if nl: print() # New Line
        print(f"{cls._timestamp(color)} {cls._color('>', color)} {cls._color(text, color)}")

    @classmethod
    def _input(cls, color: ColorOption, nl: bool = False) -> str:
        if nl: print() # New Line
        return input(f"{cls._timestamp(color)} {cls._color('>> ', color)}")

    @classmethod
    def error(cls, text: str, nl: bool = True) -> None:
        with cls._lock:
            cls._print(text, "red", nl)
            os._exit(1)

    @classmethod
    def send(cls, text: str, color: ColorOption = DefaultColor, nl: bool = False) -> None:
        with cls._lock:
            cls._print(text, color, nl)
        
    @classmethod
    def ask(cls, color: ColorOption = DefaultColor, nl: bool = False) -> str:
        with cls._lock:
            return cls._input(color, nl)

    @classmethod
    def menu(cls, title: str, options: list[str], color: ColorOption = DefaultColor) -> int:
        with cls._lock:

            cls._print(title, color, True)
            for i, option in enumerate(options):
                cls._print(f'[{i+1}] {option}', color)

            response = cls._input(color)

            if response == "":
                return 0
            
            try:
                response = int(cls._input(color))
            except ValueError:
                cls.error("Invalid Input.")
            else:
                return response
