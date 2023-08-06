PyANSIEscapes - Console Manipulation using ANSI Escapes Sequences
=========================================================================

This package provides human readable functions for adding ANSI escapes sequences to your python console outputs.
It's loosy based on [ansiescapes](https://github.com/kodie/ansiescapes), however offers more convenience functions
for formatting Rich Text.

Installation
-----------
```zsh
pip install pyansiescapes
```

Usage
------------
```python
import pyansiescapes.commands as ansi

# Print blue text on white background:
print(ansi.format("Hello ANSI!", color = 'blue', background = 'white'))

```

API-Reference
--------------
The documentation is hosted on [readthedocs.io](https://pyansiescapes.readthedocs.io/en/latest/)

You can also access the docs using `help(ansi)` in a python REPL.

License
--------------

This repository is licensed under the MIT License. See [LICENSE](./LICENSE) for details.
