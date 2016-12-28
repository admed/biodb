from biodb import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
# from django.http import HttpResponse
from mixins import ProjectPermissionMixin
from django.views import generic
from models import Project, RObject
# from guardian.shortcuts import get_objects_for_user
from guardian.mixins import PermissionRequiredMixin, PermissionListMixin, LoginRequiredMixin


# Create your views here.
def redirect_to_home(request):
    ''' In case of request '/' redirect to '/projects/' '''  
    return redirect(to=settings.HOME_URL)

class ProjectListView(LoginRequiredMixin, PermissionListMixin, generic.ListView):
    permission_required = 'projects.can_visit_project'
    template_name = 'projects/project_list.html'
    raise_exception = True
    model = Project
    context_object_name = "projects"

class RObjectListView(ProjectPermissionMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'projects.can_visit_project'
    template_name = 'projects/RObject_list.html'
    model = RObject
    context_object_name = "robjects"
    raise_exception = True
    # slug_field = "name"

    def get_queryset(self, *args, **kwargs):
        project = self.get_permission_object()
        return project.robject_set.all()



class ProjectUpdateView(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'projects.change_project'
    raise_exception = True
    model = Project
    fields = ["name", "description"]



