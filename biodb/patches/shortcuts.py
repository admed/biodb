from django.shortcuts import _get_queryset
from django.http import Http404

def get_objects_or_404(klass, *args, **kwargs):
    """
    Patch from: https://code.djangoproject.com/ticket/14150#no1

    No requires testing

    Get a set of filtered objects

    Uses filter() to return objects, or raise a Http404 exception if
    no objects matches.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the filter() query.
    """
    queryset = _get_queryset(klass)
    objects = queryset.filter(*args, **kwargs)
    if not objects:
        raise Http404('No %s matches the given query.' % queryset.model._meta.object_name)
    return objects

def get_list_or_404(klass, *args, **kwargs):
    """
    Patch from: https://code.djangoproject.com/ticket/14150#no1

    No requires testing
    
    Get a list of filtered objects

    Uses get_object_or_404 to get a set of objects, which will raise a Http404 exception if
    no objects matches, then returns that set as a list.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the filter() query
    with get_objects_or_404.
    """
    return list(get_objects_or_404(klass, *args, **kwargs))