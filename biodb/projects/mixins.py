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
    ''' Mixin for use in views, where user can search/filter models records '''

    def search(self, queryset, query, *args, **kwargs):
        return watson.filter(queryset, query)

    def filter(self, queryset, after, before):
        ''' Perform filter '''
        if after: queryset = queryset.filter(create_date__gte=after)
        if before: queryset = queryset.filter(create_date__lte=before)
        return queryset

