# django-template-breakpoint

Drop into a Python debugger from inside your Django templates.

Inspired by [django-template-debug](https://github.com/calebsmith/django-template-debug).

## Installation

Install with pip:

```
python -m pip install django-template-breakpoint
```

## Usage

Add the app to your `INSTALLED_APPS` setting:

```
INSTALLED_APPS = [
    ...,
    "django_template_breakpoint",
    ...,
]
```

In a template, load the tag:

```
{% load breakpoint %}
```

Then set the breakpoint:

```
{% breakpoint %}
```

When this line is rendered by Django, `sys.breakpointhook()` will be called.
By default, this calls `pdb.set_trace()`.

All template variables in use are added to the current scope.
If using `pdb.set_trace()`,
you can run `dir()` to see the names of all template variables.


## Development

There's a test!  Run it with `python -m pytest`.
