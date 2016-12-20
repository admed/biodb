from biodb import settings
from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from mixins import LoginRequiredMixin
from django.views import generic
from models import Project
# from guardian.shortcuts import get_objects_for_user
from guardian.mixins import PermissionRequiredMixin, PermissionListMixin


# Create your views here.
def redirect_to_home(request):
    ''' In case of request '/' redirect to '/projects/' '''  
    return redirect(to=settings.HOME_URL)

class ProjectsView(PermissionListMixin, generic.ListView):
    permission_required = 'projects.can_visit'
    template_name = 'projects/projects.html'
    raise_exception = True
    model = Project

    # def get_queryset(self):
    #     projects = get_objects_for_user(self.request.user, 'projects.can_visit')

    #     return projects

class ProjectDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'projects.can_visit'
    template_name = 'projects/project_detail.html'
    model = Project

class ProjectUpdateView(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'projects.change_project'
    raise_exception = True
    model = Project
    fields = ["name", "description"]



