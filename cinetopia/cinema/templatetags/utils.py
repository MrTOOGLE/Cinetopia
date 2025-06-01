from django import template

register = template.Library()


@register.simple_tag
def update_query_params(request, **kwargs):
    params = request.GET.copy()

    for key in kwargs.keys():
        if key in params:
            del params[key]

    params.update(kwargs)
    return params.urlencode()
