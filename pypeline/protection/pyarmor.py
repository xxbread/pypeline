
from ..util import Executor, Temp, Results, Util
from typing import Literal
import shutil
import os

class Pyarmor92:

    counter = 1
    @classmethod
    def _results(cls, mode: Literal["ecc", "rft"]) -> None:
        '''
        Collect all files in Results and replace original script with the generated one.
        '''

        original_script = Temp.path("main.py")
        pyarmor_script = os.path.join(Temp.path("dist"), "main.py")
        
        # .pyarmor config
        shutil.copytree(Temp.path(".pyarmor"), Results.path(f".pyarmor92_{mode}-{cls.counter}"))
        Util.rmTree(Temp.path(".pyarmor"), raiseError=False)

        # log result
        shutil.copy(pyarmor_script, Results.path(f".pyarmor92_{mode}-{cls.counter}.py"))

        # replace original script
        os.remove(original_script)
        shutil.copy(pyarmor_script, original_script)
        Util.rmTree(Temp.path("dist"), raiseError=False)
        cls.counter += 1

    @classmethod
    def RFT(cls) -> None:
        '''
        Build Pyarmor RFT Script. (Obfuscate Source Code With Changed Names)
        '''

        # Verify Temp Dir State (requires project files)
        Temp.verify()

        # RFT Settings
        scripts = [
            "pyarmor env -p set rft:remove_assert 1",
            "pyarmor env -p set rft:remove_docstr 1",
            "pyarmor env -p set rft:builtin_mode 1",
            "pyarmor env -p set rft:argument_mode 3",
            "pyarmor env -p set rft:export_mode 0",

            "pyarmor build --autofix 2",
            "pyarmor build --randname 1",
        ]

        # Initialize Pyarmor Environment
        Executor.run("pyarmor init -C -e main.py")

        # Setup RFT Environment
        for script in scripts:
            Executor.run(script)

        # Build RFT Script
        Executor.run("pyarmor build --rft")
        cls._results("rft")
    
    @classmethod
    def ECC(cls) -> None:
        '''
        Build Pyarmor ECC Script. Main Protection Method. 
        Documentation at: https://pyarmor.eke.org.cn/archive/v9/docs/en/user/concepts.html#term-ECC-Script
        Building ECC Requires a C compiler. # TODO: ADD DOWNLOAD LINK OR C COMPILER CHECK
        '''

        # Verify Temp Dir State (requires project files)
        Temp.verify()

        # Initialize Pyarmor Environment
        Executor.run("pyarmor init -C -e main.py")

        # Build ECC Script
        Executor.run("pyarmor build --ecc")
        cls._results("ecc")

class Pyarmor91:
    options = []
    scripts = []
    Mode = Literal["max", "min"]
    
    @classmethod
    def configure(cls, mode: Mode) -> None:

        ARGS_PRIMARY = [
            "--enable-bcc",
            "--pack main.spec"
        ]

        ARGS_PRIMARY_EXTENDED = [
            "--enable-themida",
            "--expired 90",
        ]

        ARGS_SECONDARY = [
            "--assert-call",
            "--assert-import",
            "--obf-module 1",
            "--obf-code 2",
            "--private",
            "--enable-jit",
        ]
        
        cls.options = []
        match mode:
            case "max":
                # bcc, themida, expiry, + all secondary
                cls.options.extend(ARGS_PRIMARY + ARGS_PRIMARY_EXTENDED + ARGS_SECONDARY)
            
            case "min":
                # only bcc
                cls.options.extend(ARGS_PRIMARY)

        cls.scripts = [
            'pyarmor cfg nts="pool.ntp.org,time.cloudflare.com,time.google.com,time.aws.com"', # force network for expiry
            "pyarmor cfg on_error=2", # as little error data as possible
            "pyarmor cfg enable_trace=1", # (internal) enable trace log
            f'{"pyarmor -d gen"} {" ".join(cls.options)} {" ".join(["main.py"])}' # construct final gen command
        ]

    @classmethod
    def execute(cls, wrap_main: bool = False) -> None:

        # Verify Required Project Files
        Temp.verify()
        
        ## :: Wrap Code In Main To Force BCC ::
        if wrap_main:
            # TODO
            pass
        
        ## :: Execute Scripts ::
        print()
        for script in cls.scripts:
            Executor.run(script)

        ## :: Transfer Results ::
        shutil.copy(Temp.path("pyarmor.debug.log"), Results.path(".pyarmor91_debug.log"))
        os.remove(Temp.path("pyarmor.debug.log"))

        shutil.copy(Temp.path("pyarmor.trace.log"), Results.path(".pyarmor91_trace.log"))
        os.remove(Temp.path("pyarmor.trace.log"))
        
        shutil.copy(Temp.path("main.patched.spec"), Results.path(".pyarmor91_patched.spec"))
        os.remove(Temp.path("main.patched.spec"))

        shutil.copytree(Temp.path(".pyarmor"), Results.path(".pyarmor91"))
        Util.rmTree(Temp.path(".pyarmor"), raiseError=False)

        shutil.copy(os.path.join(Temp.path("dist"), "main.exe"), Results.path("main.exe"))
        Util.rmTree(Temp.path("dist"), raiseError=False)

        # TODO: Run Debug Plugin
        # ...