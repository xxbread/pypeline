
from .util import Temp, Util, Results, Log, Executor
from .protection import Pyarmor91, Pyarmor92,Pyinstaller
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
    # Pyarmor91.configure("max")
    # Pyarmor91.execute()

    Pyarmor92.ECC()

    print()
    Log.send("Completed.", "green")
    time.sleep(999)
    # Util.rmTree(Temp.root, raiseError=False)
    
    