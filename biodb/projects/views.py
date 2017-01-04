from biodb import settings
from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse
from mixins import ProjectPermissionMixin, SearchMixin
from django.views import generic
from models import Project, RObject
# from guardian.shortcuts import get_objects_for_user
from guardian.mixins import PermissionRequiredMixin, PermissionListMixin, LoginRequiredMixin
from tables import RObjectTable
from django_tables2 import SingleTableView, SingleTableMixin
from forms import SearchFilterForm


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

class RObjectListView(ProjectPermissionMixin, PermissionRequiredMixin, SingleTableMixin, generic.FormView, SearchMixin):
    permission_required = 'projects.can_visit_project'
    template_name = 'projects/robject_list.html'
    model = RObject
    raise_exception = True
    table_class = RObjectTable
    form_class = SearchFilterForm

    def get_table_data(self):
        ''' Limit robjects to those related to project. Enable searching. ''' 

        # get project instance
        project = self.get_permission_object()
        # get all related robjects
        queryset = project.robject_set.all()

        # perforn searching
        query = self.request.GET.get("query", None)
        if query:
            queryset = self.search(queryset=queryset, query=query)

        return queryset

class ProjectUpdateView(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'projects.change_project'
    raise_exception = True
    model = Project
    fields = ["name", "description"]



