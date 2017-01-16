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
from django.forms import modelform_factory, modelformset_factory
from rebar.group import formgroup_factory

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


class RObjectListView(mixins.ProjectPermissionMixin, PermissionRequiredMixin, SingleTableMixin, generic.FormView, mixins.SearchMixin):
    permission_required = 'projects.can_visit_project'
    template_name = 'projects/robject_list.html'
    model = RObject
    # raise_exception = True
    table_class = RObjectTable
    form_class = SearchFilterForm
    success_url = "."

    def get_table_data(self):
        ''' Limit objects in table using: a) project related permission, b) searching query,
            c) date filtering '''

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
    ''' View capable to delete more than one Robject! '''

    permission_required = 'projects.can_visit_project'
    model = RObject

    def get_success_url(self):
        return reverse('projects:robject_list', kwargs={"project_name": self.kwargs["project_name"]})


class RObjectCreateView(mixins.ProjectPermissionMixin, PermissionRequiredMixin, generic.FormView):
    permission_required = 'projects.change_project'
    raise_exception = True
    model = RObject
    template_name = "projects/robject_create.html"

    def get_form_class(self):
        # create RObject model form
        RObjectForm = modelform_factory(RObject, exclude=("project","creator",))
        # create Name formset
        NameFormSet = modelformset_factory(
            Name, exclude=("robject",), formset=BaseNameFormSet, extra=1)
        # join above forms into one form using rebar's formgroup_factory
        RObjectFormGroup = formgroup_factory(
            (
                (NameFormSet, "name"),
                (RObjectForm, "robject"),
            ),
        )
        return RObjectFormGroup

    def form_valid(self, form):
        # create robject from form, but not save it!
        robject = form.robject.save(commit=False)

        # bound robject with project and User
        robject.project = self.get_permission_object()
        robject.creator = self.request.user
        
        # now save it
        robject.save()

        # the same story with names 
        names = form.name.save(commit=False)

        # iterate over names, bound to robject and save
        for name in names:
            name.robject = robject
            name.save()

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('projects:robject_list', kwargs={"project_name": self.kwargs["project_name"]})
