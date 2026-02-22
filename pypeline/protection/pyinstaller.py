
import os

IMPORTS_ENCRYPTION = [
    "cryptography.hazmat.backends",
    "cryptography.hazmat.primitives.ciphers",
    "cryptography.hazmat.primitives.ciphers.algorithms",
    "cryptography.hazmat.primitives.ciphers.modes",
    "cryptography.hazmat.primitives.padding",
]

SPEC = """
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[{imports}],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console={console},
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin={admin},
    icon='{icon}',
)
"""


class Pyinstaller:

    @classmethod
    def generateSpec(
        cls, 
        path: os.PathLike,
        imports: list[str] = [],
        console: bool = False,
        admin: bool = True,
        icon: bool = False,
        ) -> None:

        spec = SPEC.format(
            imports=", ".join(f'"{i}"' for i in imports + IMPORTS_ENCRYPTION),
            console=console,
            admin=admin,
            icon="icon.ico" if icon else "NONE",
        )

        with open(path, "w") as file:
            file.write(spec)