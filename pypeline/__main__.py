
import sys
import os
from .main import main as pypeline

if __name__ == "__main__":

    _input = os.getcwd()
    _output = os.getcwd()

    args = sys.argv[1:]
    
    try:
        _input = args[0]
    except IndexError:
        pass

    try:
        _output = args[1]
    except IndexError:
        pass
    
    try:
        pypeline(_input, _output)
    except KeyboardInterrupt:
        os._exit(1)