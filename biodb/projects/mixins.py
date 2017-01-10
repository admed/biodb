from django.shortcuts import get_object_or_404
from models import Project
from watson import search as watson


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

    @staticmethod # dont use 'self' instance inside 
    def filter(queryset, after, before):
        ''' Perform filter '''
        if after: queryset = queryset.filter(create_date__gte=after)
        if before: queryset = queryset.filter(create_date__lte=before)
        return queryset

