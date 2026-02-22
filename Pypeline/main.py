
from .util import Temp, Results, Log, Executor
from .protection import Pyarmor91, Pyinstaller
import shutil
import time

def main(path_input: str, path_output: str) -> None:

    ## :: Stage 1 :: -> Register Source Files
    # TODO: Add different modes for larger projects. Auto Bundle all into 1 main.py
    # stage1 = Log.menu("Register Project Files. Mode:", ["1x main.py"])
    Temp.load(path_input)

    # Save Original File
    Results.init(path_output)
    shutil.copy(Temp.path("main.py"), Results.path(".original.py"))

    Pyinstaller.generateSpec(Temp.path("main.spec"))

    # Test
    Pyarmor91.configure("max")
    Pyarmor91.execute()
    time.sleep(999)

    # print(path_input, path_output)
    # Executor.run(f'echo "Hello, World! > {path_output}"')
    
    