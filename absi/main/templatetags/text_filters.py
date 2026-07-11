from django import template
from django.utils.html import format_html, format_html_join


register = template.Library()


@register.filter
def wrap_words(value):
    if not value:
        return ''

    return format_html_join(
        ' ',
        '{}',
        (
            (
                word if word == '-'
                else format_html('<span class="wrapped-word">{}</span>', word),
            )
            for word in str(value).split()
        ),
    )
