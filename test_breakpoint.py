import inspect
import sys

import django
from django.conf import settings
from django.template import Context, Template


def test_breakpoint():
    # Set up Django.
    settings.configure(
        INSTALLED_APPS=["django_template_breakpoint"],
        TEMPLATES=[{"BACKEND": "django.template.backends.django.DjangoTemplates"}],
    )
    django.setup()

    # Set breakpoint hook to a function that verifies that the template variables have
    # been added to locals() as expected.
    sys.breakpointhook = verify_parent_locals

    # Build and render template.  We include a context key called "context" to ensure
    # that this special value is handled correctly.
    template_string = """
    {% load breakpoint %}

    {{ context.0 }}
    {% for item in items %}
    {% breakpoint %}
    {% endfor %}
    {{ context.1 }}
    """
    template = Template(template_string)
    context = Context({"items": ["XXX"], "context": ["Hello", "World"]})
    rendered = template.render(context)

    # Check that tag does not contribute any output to the rendered template.
    assert rendered.strip().split() == ["Hello", "World"]


def verify_parent_locals():
    frame = inspect.currentframe()
    f_locals = frame.f_back.f_locals

    assert f_locals["context"] == ["Hello", "World"]
    assert f_locals["items"] == ["XXX"]
    assert f_locals["item"] == "XXX"
    assert f_locals["forloop"]["counter0"] == 0
