Dynamic message prefixes providing execution context.

*Latest release 20200517*:
* @pfx: handle normal functions and also generators, improve behaviour with the wrapped docstring.
* @pfx_method: @pfx for methods.
* @pfxtag obsoleted by new @pfx.

The primary facility here is Pfx,
a context manager which maintains a per thread stack of context prefixes.
There are also decorators for functions.

Usage is like this:

    from cs.logutils import setup_logging, info
    from cs.pfx import Pfx
    ...
    setup_logging()
    ...
    def parser(filename):
      with Pfx("parse(%r)", filename):
        with open(filename) as f:
          for lineno, line in enumerate(f, 1):
            with Pfx("%d", lineno) as P:
              if line_is_invalid(line):
                raise ValueError("problem!")
              info("line = %r", line)

This produces log messages like:

    datafile: 1: line = 'foo\n'

and exception messages like:

    datafile: 17: problem!

which lets one put just the relevant complaint in exception and log
messages and get useful calling context on the output.
This does make for wordier logs and exceptions
but used with a little discretion produces far more debuggable results.

## Function `gen(func)`

Decorator for generators to manage the Pfx stack.

Before running the generator the current stack height is
noted.  After yield, the stack above that height is trimmed
and saved, and the value yielded.  On recommencement the saved
stack is reapplied to the current stack (which may have
changed) and the generator continued.

## Class `Pfx`

A context manager to maintain a per-thread stack of message prefixes.

### Method `Pfx.__init__(self, mark, *args, **kwargs)`

Initialise a new Pfx instance.

Parameters:
* `mark`: message prefix string
* `args`: if not empty, apply to the prefix string with `%`
* `absolute`: optional keyword argument, default `False`. If
  true, this message forms the base of the message prefixes;
  earlier prefixes will be suppressed.
* `loggers`: which loggers should receive log messages.

*Note*:
the `mark` and `args` are only combined if the `Pfx` instance gets used,
for example for logging or to annotate an exception.
Otherwise, they are not combined.
Therefore the values interpolated are as they are when the `Pfx` is used,
not necessarily as they were when the `Pfx` was created.
If the `args` are subject to change and you require the original values,
apply them to `mark` immediately, for example:

    with Pfx('message %s ...' % (arg1, arg2, ...)):

This is a bit more expensive as it incurs the formatting cost
whenever you enter the `with` clause.
The common usage is:

    with Pfx('message %s ...', arg1, arg2, ...):

## Function `pfx(*da, **dkw)`

General purpose @pfx for generators, methods etc.
Pfx needs a .overPfx attribute to hook up chained Pfx stacks.

Parameters:
* `func`: the function to decorate
* `message`: optional prefix to use instead of the function name
* `message_args`: optional arguments to embed in the preifx using `%`

Example usage:

    @pfx
    def f(....):
        ....

## Function `pfx_iter(tag, iterable)`

Wrapper for iterables to prefix exceptions with `tag`.

## Function `pfx_method(*da, **dkw)`

Decorator to provide a `Pfx` context for an instance method prefixing
*classname.methodname*
(or `str(self).`*methodname* if `use_str` is true).

Example usage:

    class O:
        @pfx_method
        def foo(self, .....):
            ....

## Class `PfxCallInfo(Pfx)`

Subclass of Pfx to insert current function an caller into messages.

## Function `PfxThread(target=None, **kw)`

Factory function returning a Thread
which presents the current prefix as context.

## Function `prefix()`

Return the current Pfx prefix.

## Function `PrePfx(tag, *args)`

Push a temporary value for Pfx._state._ur_prefix to enloundenify messages.

## Function `XP(msg, *args, **kwargs)`

Variation on `cs.x.X`
which prefixes the message with the current Pfx prefix.

## Function `XX(prepfx, msg, *args, **kwargs)`

Trite wrapper for `XP()` to transiently insert a leading prefix string.

Example:

    XX("NOTE!", "some message")

# Release Log



*Release 20200517*:
* @pfx: handle normal functions and also generators, improve behaviour with the wrapped docstring.
* @pfx_method: @pfx for methods.
* @pfxtag obsoleted by new @pfx.

*Release 20191004*:
@pfx_method: new optional `use_str` parameter to use str(self) instead of type(self).__name__; now requires @cs.deco.decorator

*Release 20190905*:
* Pfx.__exit__: simplify prefixify_exc() logic, prefixify all suitable attributes.
* New @pfx_method decorator for instance methods.

*Release 20190607*:
Pfx.__exit__ improved exception attribute handling.

*Release 20190403*:
Debugging aid: Pfx.umark: emit stack traceback on format conversion error.

*Release 20190327*:
* @pfx: set __name__ on the wrapper function.
* Bugfix some references to the internal prefixify function.

*Release 20190324*:
Pfx.__exit__: apply the prefix to all the standard attributes where present, improves some message behaviour for some exception types.

*Release 20181231*:
Bugfix for an infinite regress.

*Release 20181109*:
* Update @contextmanager formalism to use try/finally for the cleanup phase.
* New decorator @gen to manage Pfx state across generator iterations; pretty clunky.
* Better fallback handling.
* Some docstring updates.

*Release 20170910*:
Slight linting.

*Release 20170903.1*:
corrections to the module docstring

*Release 20170903*:
Initial release for PyPI.
