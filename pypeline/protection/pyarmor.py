
from ..util import Executor, Log, Temp, Results, Util
from typing import Literal
import shutil
import os

class Pyarmor92:
    
    @classmethod
    def protect(cls) -> None:
        pass

class Pyarmor91:
    options = []
    scripts = []
    Mode = Literal["max", "min"]
    
    @classmethod
    def configure(cls, mode: Mode) -> None:
        cls.options = []

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
    def execute(cls, wrap_main: bool = True) -> None:
        
        ## :: Wrap Code In Main To Force BCC ::
        if wrap_main:
            # TODO
            pass
        
        ## :: Execute Scripts ::
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