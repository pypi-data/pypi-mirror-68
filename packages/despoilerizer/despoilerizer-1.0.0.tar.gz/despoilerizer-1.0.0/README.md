# Despoilerizer

This script reads from stdin and prints out the contents of stdin to stdout,
without the lines that are in between the `:SPOILERS BEGIN:` and the
`:SPOILERS END:` tags.

It uses stdin and stdout so that it can be easily integrated in bash 
scripting, for instance:
```bash
$ <my_file.tex | python despoilerizer.py | pdflatex
```

You can also redefine the tags:

```bash
$ <my_file.tex | \
  python despoilerizer.py --begin="# spoiler" --end="# unspoiler" | \
  pdflatex
```

## Installation

```bash
$ pip install despoilerizer
```

## Examples

#### stdin
```
This is a simple file.
:SPOILERS BEGIN:
It contains spoilers.
:SPOILERS END:
And also other information.
```

#### stdout
```
This is a simple file.
And also other information.
```

#### stdin
```
\begin{document}
% :SPOILERS BEGIN:
important stuff...
% :SPOILERS END:
\end{document}
```

#### stdout
```
\begin{document}
\end{document}
```

## Usage as importable package

```python
import despoilerizer
from pathlib import Path as P

for path in [P('file1.tex'), P('file2.py'), P('file3.txt')]:
    out_path = P(path.stem + '_nospoilers' + path.suffix)
    with open(path, 'r') as fin:
        with open(out_path, 'w') as fout:
            despoilerizer.despoilerize_file(fin, fout)


contents = """
This is a very important string.
such spoilers
I really don't want anyone to know.
much wow
"""

with open(P('some_file.txt'), 'w') as f:
    f.write(
        despoilerizer.despoilerize(contents, begin='such spoilers', end='much wow')
    )
```

## Motivation

I have a LaTeX file for a document I'm sharing with my friends.
This document contains some information for a DnD campaign both for stuff the 
players have encountered and stuff that's being worked on.

Therefore, I want to have two different PDF documents: one with the spoilers
and one without them.
