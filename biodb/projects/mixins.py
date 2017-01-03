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
    ''' Mixin for use in views, where user can search through model/models records '''

    def search(self, queryset, query, *args, **kwargs):
        return watson.filter(queryset, query)

