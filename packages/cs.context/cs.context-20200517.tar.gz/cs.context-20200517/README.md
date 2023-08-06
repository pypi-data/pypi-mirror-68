Context managers. Initially just `stackattrs`.

*Latest release 20200517*:
* Add `nullcontext` like the one from recent contextlib.
* stackattrs: expose the push and pop parts as pushattrs() and popattrs().

## Function `popattrs(o, attr_names, old_values)`

The "pop" part of stackattrs.
Restore previous attributes of `o`
named by `attr_names` with previous state in `old_values`.

## Function `pushattrs(o, **attr_values)`

The "push" part of stackattrs.
Push `attr_values` onto `o` as attributes,
return the previous attribute values in a dict.

## Function `stackattrs(o, **attr_values)`

Context manager to push new values for the attributes of `o`
and to restore them afterward.
Returns a `dict` containing a mapping of the previous attribute values.
Attributes not present are not present in the mapping.

Restoration includes deleting attributes which were not present
initially.

Example of fiddling a programme's "verbose" mode:

    >>> class RunModes:
    ...     def __init__(self, verbose=False):
    ...         self.verbose = verbose
    ...
    >>> runmode = RunModes()
    >>> if runmode.verbose:
    ...     print("suppressed message")
    ...
    >>> with stackattrs(runmode, verbose=True):
    ...     if runmode.verbose:
    ...         print("revealed message")
    ...
    revealed message
    >>> if runmode.verbose:
    ...     print("another suppressed message")
    ...

Example exhibiting restoration of absent attributes:

    >>> class O:
    ...     def __init__(self):
    ...         self.a = 1
    ...
    >>> o = O()
    >>> print(o.a)
    1
    >>> print(o.b)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'O' object has no attribute 'b'
    >>> with stackattrs(o, a=3, b=4):
    ...     print(o.a)
    ...     print(o.b)
    ...     o.b = 5
    ...     print(o.b)
    ...     delattr(o, 'a')
    ...
    3
    4
    5
    >>> print(o.a)
    1
    >>> print(o.b)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'O' object has no attribute 'b'

# Release Log



*Release 20200517*:
* Add `nullcontext` like the one from recent contextlib.
* stackattrs: expose the push and pop parts as pushattrs() and popattrs().

*Release 20200228.1*:
Initial release with stackattrs context manager.
