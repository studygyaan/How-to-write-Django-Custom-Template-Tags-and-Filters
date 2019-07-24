from django import template

register = template.Library()


from django.template.defaultfilters import stringfilter
@register.filter(name='lower')
@stringfilter
def lower(value):
    return value.lower()


@register.filter(is_safe=True)
def myfilter(value):
    return value


from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
@register.filter(needs_autoescape=True)
def initial_letter_filter(text, autoescape=True):
    first, other = text[0], text[1:]
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    result = '<strong>%s</strong>%s' % (esc(first), esc(other))
    return mark_safe(result)


# tags
from datetime import datetime
@register.simple_tag
def current_time(format_string):
    return datetime.now().strftime(format_string)


register.simple_tag(lambda x: x - 1, name='minusone')


@register.simple_tag(name='minustwo')
def some_function(value):
    return value - 2


@register.simple_tag
def my_tag(a, b, *args, **kwargs):
    warning = kwargs['warning']
    profile = kwargs['profile']
    return warning


from django.contrib.auth.models import User
@register.inclusion_tag('results.html')
def show_results():
      obj = User.objects.values_list('username', flat=True)
      return {'choices': obj}
