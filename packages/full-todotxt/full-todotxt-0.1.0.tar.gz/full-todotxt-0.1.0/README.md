full-todotxt
======

[todotxt](http://todotxt.org/) interactive interface that forces you to specify certain attributes.

For each todo, you have to specify at least `one project tag` (e.g. `+work`) and a priority `(A)`.

Though not required for each todo, it will prompt you want to specify a `deadline`, which will store a `deadline` key-value pair to the todo with the datetime as the value.

For example:

```
(A) measure space for shelving +home deadline:2020-05-13-15-30
```

... which specifies 2020-05-13 at 3:30PM.

This can be used with `full-todotxt-server`, which parses the config file and sends you reminders whenever a `deadline` is approaching.

Installation
------------

#### Requires:

`python3.6+`

To install with pip, run:

    pip3 install full_todotxt

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

