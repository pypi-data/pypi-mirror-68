full-todotxt
======

[![PyPi version](https://img.shields.io/pypi/v/full_todotxt.svg)](https://pypi.python.org/pypi/full_todotxt) [![Python 3.6|3.7](https://img.shields.io/pypi/pyversions/full_todotxt.svg)](https://pypi.python.org/pypi/full_todotxt)

[todotxt](http://todotxt.org/) interactive interface that forces you to specify certain attributes.

<img src="https://raw.githubusercontent.com/seanbreckenridge/full_todotxt/master/.github/demo.gif" alt="demo gif">

For each todo, you have to specify at least `one project tag` (e.g. `+work`) and a priority `(A)`.

Though not required for each todo, it will prompt you want to specify a `deadline`, which will store a `deadline` key-value pair to the todo with the datetime as the value.

For example:

```
(A) measure space for shelving +home deadline:2020-05-13-15-30
```

... which specifies 2020-05-13 at 3:30PM.

I use this with [`todotxt_deadline_notify`](https://github.com/seanbreckenridge/todotxt_deadline_notify), which parses the todo.txt file and sends me a reminders whenever a `deadline` is approaching.

Installation
------------

#### Requires:

`python3.6+`

To install with pip, run:

    pip3 install full-todotxt

Run
----------

```
Usage: full_todotxt [OPTIONS] TODOTXT_FILE

Options:
  --add-due           Add due: key/value flag based on deadline:
  --time-format TEXT  Specify a different time format for deadline:
  --help              Show this message and exit.
```

Example:

```
full_todotxt ~/.todo/todo.txt
```

