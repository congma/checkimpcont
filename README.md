[![Build Status](https://travis-ci.org/congma/checkimpcont.svg?branch=master)](https://travis-ci.org/congma/checkimpcont)

## `checkimpcont.py` ##

Check concatenated string literals in Python source code.


## Usage ##

```
checkimpcont.py [file]
```

## Example ##

The example applies the script to its own source.
```
checkimpcont.py checkimpcont.py
```

It detects one warning:
```
41:43: warning: string literal concatenation
    print("%s:%s: warning: string literal "
                                        ~~~^
```

## Installation ##

```bash
python setup.py install
# -- or --
pip install .
```

## Rationale ##

Like C, Python allows adjacent string literals to be implicitly concatenated.
In particular, this can happen to strings on different lines.  Sometimes, this
can be confusing when initializing a sequence, for instance,
```python
L = ["spam",
     "eggs"
     "ham"]
```
This above list has two elements, `"spam"` and `"eggsham"`, but it might not be
obvious at first glance.

See also the StackOverflow posts:  
*  [Issue warning for missing comma between list items bug](https://stackoverflow.com/questions/34540634/issue-warning-for-missing-comma-between-list-items-bug)
*  [Can I get a lint error on implicit string joining in python?](https://stackoverflow.com/questions/40503153/can-i-get-a-lint-error-on-implicit-string-joining-in-python)

The implementation uses a pushdown machine to detect the `STRING` tokens
followed by `NL` tokens that should be picked out (not all of them are).  A
pushdown machine may be a bit overkill, but I hate nested `if`s and `elif`s.

This situation is analogous to the one found in the book <i>Expert C
Programming</i>, Chapter 2, by Peter van der Linden:
```c
char *available_resources[] = {
    "color monitor",
    "big disk",
    "Cray" /*           whoa! no comma! */
    "on-line drawing routines",
    "mouse",
    "keyboard",
    "power cables",     /* and what's this extra comma? */
};
```
It would be a mistake to assume the resources include a Cray supercomputer.


## See Also ##

[vim-checkimpcont](https://github.com/congma/vim-checkimpcont), a Vim plugin.


## License ##

The code is in public domain.
