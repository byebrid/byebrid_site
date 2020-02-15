from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """Handy tag to keep parameters in the url whilst making additions/changes.
    Initially created so we can paginate searches. I.e. if you want to get the
    last page of search results.

    Thanks to answers from this stackoverflow: 
    https://stackoverflow.com/questions/2047622/how-to-paginate-django-with-other-get-variables/57899037#57899037
    """
    query = context['request'].GET.copy()
    query.update(kwargs)
    # This is required since `query` is actually a QueryDict, whose update()
    # method is not like the usual dict.update(). query['page'] is actually a 
    # list and when you call update on it, it appends to that list, instead of
    # just resetting the item. Very strange.
    if 'page' in query and 'page' in kwargs:
        query.__setitem__('page', kwargs['page'])
    return query.urlencode()