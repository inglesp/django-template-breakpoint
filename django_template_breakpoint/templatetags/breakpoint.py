import builtins
import sys

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def breakpoint(context):  # noqa: A001
    """Invoke the breakpoint hook.

    Since this function's parameter must be called `context`, we call another function
    to do the work

    This calls a separate function because this function is decorated with
    `takes_context = True`, which means that its first parameter must be called
    `context`.  However...
    """

    _breakpoint(context)

    # Return empty string, so that nothing is rendered in the template.
    return ""


def _breakpoint(_context):
    """Actually do the work."""

    # Add each template variable in the context to locals().  Inside the body of a
    # function, existing keys in locals() cannot be overwritten, but new keys can be
    # added.
    #
    # Because (a) all variables in this function begin with an underscore, and (b)
    # template variables cannot begin with an underscore, there is no danger that a
    # template variable will not be added to locals()
    for _k, _v in _context.flatten().items():
        locals()[_k] = _v

    # Invoke the breakpoint hook.  By default, this calls pdb.set_trace().
    builtins.breakpoint()
