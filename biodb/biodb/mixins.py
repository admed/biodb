from django.shortcuts import get_object_or_404
from patches.shortcuts import get_objects_or_404
from projects.models import Project
from watson import search as watson
from django.views.generic.edit import DeletionMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.views.generic import DeleteView 

class ProjectPermissionMixin():
    ''' Mixin prepared for check user permission to any view contains data related to given project '''

    def get_permission_object(self):
        ''' Return specyfic Project instance for permission check. '''

        project = get_object_or_404(Project, name=self.kwargs["project_name"])
        return project


class SearchMixin():
    ''' Mixin for use in views, where user can search/filter models records. Methods customized 
        to work with different types of models. '''

    def search(self, queryset, query, *args, **kwargs):
        ''' Perform search '''
        return watson.filter(queryset, query)

    @staticmethod  # dont use 'self' instance inside
    def filter(queryset, after, before):
        ''' Perform filter '''
        if after:
            queryset = queryset.filter(create_date__gte=after)
        if before:
            queryset = queryset.filter(create_date__lte=before)
        return queryset


class DeleteMultipleView(DeleteView):
    """
    View for deleting an objects included in QuerySet object retrieved with `self.get_object()`,
    with a response rendered by template.
    """
    pk_separate_by = "+"

    def get_object(self):
        ''' Here object will be QuerySet not model instance ''' 

        ids = self.kwargs["robject_ids"].split(self.pk_separate_by)

        return get_objects_or_404(self.model, pk__in=ids)