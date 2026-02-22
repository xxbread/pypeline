
from . import Util, Log
import os
import time
import shutil

class Results:
    root = ""

    @classmethod
    def init(cls, path: os.PathLike) -> None:
        name = f".build_{int(time.time())}"
        cls.root = os.path.join(path, name)
        os.makedirs(cls.root, exist_ok=True)

    @classmethod
    def path(cls, name: str) -> str:
        return os.path.join(cls.root, name)

class Temp:
    path_file = os.path.realpath(__file__)
    path_dir = os.path.dirname(path_file)
    root = os.path.join(os.path.dirname(path_dir), "_temp")
    Util.rmTree(root, raiseError=True)
    os.makedirs(root, exist_ok=True)

    @classmethod
    def path(cls, name: str) -> str:
        return os.path.join(cls.root, name)

    @classmethod
    def load(cls, path: os.PathLike) -> None:

        sufficient = False
        for entry in os.listdir(path):
            
            if entry == "main.py":
                Log.send("[+] main.py", "green")
                shutil.copy(os.path.join(path, entry), cls.path(entry))
                sufficient = True
            
            elif entry == "icon.ico":
                Log.send("[+] icon.ico", "green")
                shutil.copy(os.path.join(path, entry), cls.path(entry))

            else:
                Log.send(f"[-] {entry} (currently unsupported)", "grey")

        if not sufficient:
            Log.error("Missing main.py entry point.")
