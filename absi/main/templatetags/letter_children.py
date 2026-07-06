from django import template


register = template.Library()


@register.simple_tag
def letter_children(children, query):
    sections = {
        'short vowels': slice(0, 3),
        'long vowels': slice(3, 7),
        'diphthongs': slice(7, 10),
        'other': slice(10, None),
    }
    return children[sections.get(query, slice(0, 0))]
