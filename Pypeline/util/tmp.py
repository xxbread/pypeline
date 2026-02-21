
import os

class Tmp:
    path_file = os.path.realpath(__file__)
    path_dir = os.path.dirname(path_file)
    root = os.path.join(os.path.dirname(path_dir), "_temp")
    os.makedirs(root, exist_ok=True)

    @classmethod
    def path(cls, name: str) -> str:
        return os.path.join(cls.root, name)