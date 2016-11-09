from django import template
from django.core import urlresolvers

register = template.Library()


@register.simple_tag(takes_context=True)
def current(context, url_name, method, return_value=' active', **kwargs):

    if method == 'ns':
        return_value = 'active'

    if method == 'ul':
        return_value = 'show'

    matches = current_url_equals(context, url_name, method, **kwargs)
    return return_value if matches else ''


# PARA FUNCIONAR A VIEW TEM QUE PASSAR UM REQUEST
def current_url_equals(context, url_name, method, **kwargs):
    resolved = False

    try:
        resolved = urlresolvers.resolve(context.get('request').path)
    except:
        pass

    #Namespace
    if method == 'ns':
        matches = resolved and resolved.namespace == url_name

    #Name
    elif method == 'n':
        matches = resolved and resolved.url_name == url_name

    #Namespace & Name
    else:
        matches = resolved and resolved.namespace + ':' + resolved.url_name == url_name

    if matches and kwargs:
        for key in kwargs:
            kwarg = kwargs.get(key)
            resolved_kwarg = resolved.kwargs.get(key)
            if not resolved_kwarg or kwarg != resolved_kwarg:
                return False
    return matches
