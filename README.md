

### [Python]() [License]()

### [Introduction](#Introduction) • [Usage](#Usage) • [License](#License)



---

# Introduction

Pypeline is a .py to .exe pipeline tool that utilizes and merges different methods of protecting python source code.

It is known that Python isnt the right choice for deploying native applications, mainly because of its poor ways of protecting its sourcecode. However, that doesnt mean that its impossible. The goal of this project is not to deny Pythons mentioned limitations, but rather to protect native applications in the best possible way while keeping the benefit of using Python. 

The most common way to pack a Python project into a .exe is by using [Pyinstaller](https://pypi.org/project/pyinstaller/).

Pyinstaller takes the sourcecode (ex. `main.py` , or any other combination of files) and compiles it into .pyc, which is simply [Python Bytecode](https://realpython.com/ref/glossary/bytecode/). That Python bytecode is bundled into an archive that contains a python runtime, pythons builtins, your code, and additional data files. This archive is wrapped by a Native Bootloader made in C++ which executes your Python Code with the bundled interpreter. 

Simplified that makes it:

1. `main.py`
2. `main.pyc`
3. `Bundled: [Native bootloader + py runtime + py libraries + main.pyc + datas]`
4. `main.exe`

But because Pyinstaller was made for simple deployment, not protection, that archive can easily be extracted and the Python Byte Code can be viewed. The Byte Code can be reverted back into Source Code quite reliably. 

... to be continued.

# Usage

### Download:

`git clone https://github.com/xxbread/pypeline/`
`cd pypeline`

### Pip Install:

```
pyinstaller==6.15.0
pyarmor.cli==9.2.3
cryptography==44.0.2
...
```
Please match the specific versions to avoid risks.

### Other Requirements:

If you want to use the core Pyarmor features (recommended):

- [Pyarmor Pro License (or better)](https://jondy.github.io/paypal/index.html)

### Run:

`python -m pypeline <optional:input_path> <optional:output_path>`

If `input_path` isnt specified, the current working directory will be used.

# License

This project is licensed under the [GNU Affero General Public License v3.0 (AGPLv3)](https://github.com/xxbread/pypeline/blob/main/LICENSE).