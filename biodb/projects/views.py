from biodb import settings
from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.views import generic
from models import Project, RObject
# from guardian.shortcuts import get_objects_for_user
from guardian.mixins import PermissionRequiredMixin, PermissionListMixin, LoginRequiredMixin
from biodb import mixins
from tables import RObjectTable
from django_tables2 import SingleTableMixin
from forms import SearchFilterForm, RObjectCreateForm

# from django.http import HttpResponse
from django.core.urlresolvers import reverse
# from django.shortcuts import get_object_or_404, get_list_or_404
# from django.http import Http404
# from patches.shortcuts import get_objects_or_404


def redirect_to_home(request):
    """
    Set a list of projects (url: /projects) as a main url to redirect.
    """
    return redirect(to=settings.HOME_URL)


# Project Views

class ProjectListView(LoginRequiredMixin, PermissionListMixin, generic.ListView):
    """
    Show a user list of projects which has a permission to visit
    """
    permission_required = 'projects.can_visit_project'
    template_name = 'projects/project_list.html'
    raise_exception = True
    model = Project
    context_object_name = "projects"

class ProjectUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """
    View for edit project data.
    Required permission for changing.
    """
    permission_required = 'projects.change_project'
    raise_exception = True
    model = Project
    fields = ["name", "description"]

# Robject views

class RObjectListView(mixins.ProjectPermissionMixin, PermissionRequiredMixin, SingleTableMixin, generic.FormView, mixins.SearchMixin):
    """
    View of table of ROjects asigned for the project.
    Required user permision to visit project.
     - Searching options
     - Actions
     - Download Manager
    """
    permission_required = 'projects.can_visit_project'
    template_name = 'projects/robject_list.html'
    model = RObject
    # raise_exception = True
    table_class = RObjectTable
    form_class = SearchFilterForm
    success_url = "."

    def get_table_data(self):
        """
        Limit objects in table as result to: 
            a) project related permission, 
            b) searching query 
        """

        # include permissions

        # get project instance
        project = self.get_permission_object()
        # get all related robjects
        queryset = project.robject_set.all()

        if hasattr(self, "cleaned_data"):
            # include searching
            queryset = self.search(queryset=queryset, query=self.query)
            # include filtering
            queryset = self.filter(
                queryset=queryset, after=self.after_date, before=self.before_date)

        return queryset

    def form_valid(self, form):
        self.cleaned_data = form.cleaned_data

        # store data from form.cleaned_data as instance attrs
        for key, value in form.cleaned_data.iteritems():
            setattr(self, key, value)

        context = self.get_context_data()

        # display form instead of redirect
        context.update({'form': self.form_class()})

        return render(self.request, self.template_name, context)

    def post(self, request, **kwargs):
        ''' If user come from actions-form, create new url using request.POST and redirect '''

        # get POST dict
        POST = request.POST.copy()

        # pop 'actions-form' from request.POST (False if none)
        actions_form = POST.pop("actions-form", False)

        if actions_form and POST:  # check if POST not empty!
            # delete token
            del POST["csrfmiddlewaretoken"]
            # collect robject id's
            ids = POST.keys()
            # create url
            url = self.create_url(ids)
            # redirect
            return redirect(url)

        return super(RObjectListView, self).post(request, **kwargs)

    def create_url(self, ids):
        # separate id's by "+" sign
        robject_ids = "+".join(ids)

        return reverse("projects:robject_delete", kwargs={
            "robject_ids": robject_ids,
            "project_name": self.kwargs["project_name"]
        })


class RObjectDeleteView(mixins.ProjectPermissionMixin, PermissionRequiredMixin, mixins.DeleteMultipleMixin, generic.DeleteView):
    """
    Delete one or more RObjects
    """

    permission_required = 'projects.can_visit_project'
    model = RObject

    def get_success_url(self):
        return reverse('projects:robject_list', kwargs={"project_name": self.kwargs["project_name"]})



class RObjectDetailView(generic.DetailView):
    """
    Show detail view of Robject instance 
    (all fields from model + Relations to other models)
    """
    model = RObject

class RObjectUpdate(LoginRequiredMixin, generic.UpdateView):
    """
    View for updating Robject model data.
    """
    
    model = RObject
    form_class = RObjectCreateForm
    template_name_suffix = "_update"
    context_object_name = "object"

    def post(self, request, project_name, pk):
        # fetch updated object
        robject = self.get_object()

        # create files list from request data
        files = request.FILES.getlist('files')

        # save every file in db, update db relations
        for f in files:
            robject.files_set.create(file=f, rboject=robject)

        return super(RObjectUpdate, self).post(self, request)

    def form_valid(self, form):
        form.instance.changed_by = self.request.user
        return super(RObjectUpdate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # add files to context
        context = super(RObjectUpdate, self).get_context_data(**kwargs)
        context['project_name'] = self.kwargs["project_name"]
        # context['files'] = self.object.files_set.all()
        return context