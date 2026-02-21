
from . import Log, Tmp
import subprocess
import sys

class Executor:
    cwd = Tmp.root
    debug = True
    seperated = True
    output = None

    @classmethod
    def new_output(cls) -> None:
        
        cls.output = subprocess.Popen(
            [
                sys.executable,
                "-u", # unbuffered
                "-c", # command
                "import sys, ctypes\n"
                "ctypes.windll.kernel32.SetConsoleTitleW('Pypeline Executor')\n"
                "for line in sys.stdin:\n"
                "   print(line, end='', flush=True)"
            ],
            stdin=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE,
            text=True,
        )

    @classmethod
    def run(cls, command: str) -> None:

        # Optional: Track currently executing command
        if cls.debug:
            Log.send(f"Executing: [{command}]", "grey")

        # #1 Non Seperated Output
        if not cls.seperated:
            subprocess.run(
                command,
                shell=True,
                check=True,
            )
        
        # #2 Seperated Output
        else:

            if not cls.output:
                cls.new_output()

            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

            for line in process.stdout:
                cls.output.stdin.write(line)
                cls.output.stdin.flush()

            process.wait()
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, command)
