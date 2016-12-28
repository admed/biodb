from django.shortcuts import get_object_or_404
from models import Project


class ProjectPermissionMixin():
    ''' Mixin prepared for check user permission to any view contains data related to given project '''

    def get_permission_object(self): 
        ''' Return specyfic Project instance for permission check. '''

        project = get_object_or_404(Project, name=self.kwargs["project_name"])
        return project