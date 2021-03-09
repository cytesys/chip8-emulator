[![CodeQL](https://github.com/cytesys/chip8-emulator/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/cytesys/chip8-emulator/actions/workflows/codeql-analysis.yml)
# CHIP8 Emulator
This is a CHIP8 emulator written in python. It works without installing any third-party libraries.
Python 3 is required, python 3.8 or higher is recommended.

## Usage
You need to run main.py with the path to the file as the argument.
```bash
py main.py <file>
```

### Keyboard
The original CHIP8 keys are listed on the left side, and the corresponding keyboard keys are on the right:
```
CHIP8     |   Keyboard
1 2 3 C   |   1 2 3 4
4 5 6 D   |   Q W E R
7 8 9 E   |   A S D F
A 0 B F   |   Z X C V
```

## ROMs
There are a few ROMs in the roms folder, but I do not own any of them. They were copied from [dmatlack's github repository](https://github.com/dmatlack/chip8/tree/master/roms).