"""
easyinput package
https://github.com/jutge-org/easyinput
"""

from easyinput.tokenizer import *

# current version
version = "2.4"

# Specify what to import with *:
__all__ = [
    'read',
    'read_many',
    'read_line',
    'read_many_lines',
    'set_eof_handling',
    'EOFModes',
]
