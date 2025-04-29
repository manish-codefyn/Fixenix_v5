from django import template

register = template.Library()

@register.filter
def to_range(value):
    """Converts a number into a range (used for iterating in templates)."""
    try:
        return range(int(value))
    except ValueError:
        return []


@register.filter
def to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0  # Return a default value if conversion fails


@register.filter(name='add_class')
def add_class(value, arg):
    """
    Adds a CSS class to a form field.
    Usage: {{ form.field|add_class:"form-control" }}
    """
    return value.as_widget(attrs={"class": arg})


@register.filter(name='add_placeholder')
def add_placeholder(field, placeholder_text):
    """Add a placeholder attribute to form fields."""
    field.field.widget.attrs.update({"placeholder": placeholder_text})
    return field


@register.filter
def split(value, delimiter="\n"):
    """
    Splits the input string by the given delimiter and returns a list.
    Default delimiter is a newline.
    """
    return value.split(delimiter)