
import os
import stat

class Util:

    @staticmethod
    def rmReadonly(path: os.PathLike) -> None:
        try:
            os.chmod(path, stat.S_IWRITE)
        except:
            pass

    @staticmethod
    def rmTree(path: os.PathLike, raiseError: bool = False) -> None:
        
        if not os.path.exists(path):
            return
        
        if os.path.isfile(path) or os.path.islink(path):
            Util.rmReadonly(path)
            try:
                os.remove(path)
            except Exception as e:
                if raiseError:
                    raise e

        elif os.path.isdir(path):
            for entry in os.listdir(path):
                Util.rmTree(os.path.join(path, entry), raiseError)
            
            Util.rmReadonly(path)
            try:
                os.rmdir(path)
            except Exception as e:
                if raiseError:
                    raise e