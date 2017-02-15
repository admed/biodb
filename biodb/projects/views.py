from biodb import settings
from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.views import generic
from models import Project, RObject, Name
# from guardian.shortcuts import get_objects_for_user
from guardian.mixins import PermissionRequiredMixin, PermissionListMixin, LoginRequiredMixin
from biodb import mixins
from tables import RObjectTable
from django_tables2 import SingleTableMixin
from forms import SearchFilterForm, BaseNameFormSet
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import Http404
from patches.shortcuts import get_objects_or_404
from django.forms import modelform_factory, modelformset_factory, inlineformset_factory, formset_factory
from rebar.group import formgroup_factory
from forms import NameForm, RObjectForm
import re


# Create your views here.
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

    def get_context_data(self, **kwargs):
        context = super(RObjectListView, self).get_context_data(**kwargs)
        context.update({
            "kwargs": self.kwargs
        })
        return context


class RObjectDetailView(mixins.ProjectPermissionMixin, PermissionRequiredMixin, generic.DetailView):
    """
        Show detail view of Robject instance 
        (all fields from model + Relations to other models)
    """
    permission_required = ['projects.can_visit_project']
    model = RObject
    raise_exception = True


class RObjectDeleteView(mixins.ProjectPermissionMixin, PermissionRequiredMixin, mixins.DeleteMultipleMixin, generic.DeleteView):
    """
    Delete one or more RObjects
    """

    permission_required = ['projects.can_visit_project',
                           'projects.can_modify_project_content']
    model = RObject
    raise_exception = True

    def get_success_url(self):
        return reverse('projects:robject_list', kwargs={"project_name": self.kwargs["project_name"]})


class RObjectCreateView(mixins.ProjectPermissionMixin, PermissionRequiredMixin, mixins.MutableMultipleFormMixin, generic.FormView):
    permission_required = ['projects.can_visit_project',
                       'projects.can_modify_project_content']
    raise_exception = True
    forms = [(NameForm, "name-1"), (RObjectForm, "robject")]
    cloneable_forms = {"name":NameForm}
    template_name = "projects/robject_create.html"
    formgroup_context_name = "formgroup"

    def get_success_url(self):
        return reverse('projects:robject_list', kwargs={"project_name": self.kwargs["project_name"]})

    def form_valid(self, form):
        robject = form.robject.save(commit=False)
        robject.save()
        for iform in form:
            if "name" in iform.prefix:
                name = iform.save(commit=False)
                name.robject = robject
                name.save()

        return redirect(self.get_success_url())

class RObjectUpdateView(mixins.ProjectPermissionMixin, PermissionRequiredMixin, generic.TemplateView):
    permission_required = ['projects.can_visit_project',
                           'projects.can_modify_project_content']
    raise_exception = True
    # model = RObject
    template_name = "projects/robject_update.html"
    # fields = "__all__"

    # def get_form_class(self):
    #     RObjectInlineFormSet = inlineformset_factory(
    #         RObject, Name, fields=('title', 'primary'), extra=1)

    #     self.form_class = RObjectInlineFormSet
    #     return RObjectInlineFormSet

    # def form_valid(self, form):
    #     if form.deleted_forms:
    #         form.save()
    #         new_form = self.form_class(instance=self.object)
    #         context = self.get_context_data()
    #         context.update({
    #                 "form":new_form
    #             })
    #         return render(self.request, self.template_name, context)
    #     else:
    #         return super(RObjectUpdateView, self).form_valid(form)

    def get(self, request, **kwargs):
        return HttpResponse("Here, new robject update form will be build!")

    def get_success_url(self):
        return reverse('projects:robject_list', kwargs={"project_name": self.kwargs["project_name"]})
