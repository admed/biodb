from django.shortcuts import get_object_or_404
from patches.shortcuts import get_objects_or_404
from projects.models import Project
from watson import search as watson
from rebar.group import formgroup_factory
from django.views import generic
import re
from django.core.exceptions import ImproperlyConfigured
# from django.views.generic.edit import DeletionMixin
# from django.core.exceptions import ImproperlyConfigured
# from django.http import HttpResponseRedirect
# from django.views.generic import DeleteView


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

    @staticmethod  # dont use 'self' instance inside
    def filter(queryset, after, before):
        ''' Perform filter '''
        if after:
            queryset = queryset.filter(create_date__gte=after)
        if before:
            queryset = queryset.filter(create_date__lte=before)
        return queryset


class DeleteMultipleMixin():
    """
    Mix it with DeleteView to allow multiple objects deletion ability.
    """
    pk_separate_by = "+"  # separation sign in url

    def get_object(self):
        ''' 
            Extract id's from url part using separator and use them to filter robjects.
            Raise 404 if no results.
        '''

        ids = self.kwargs["robject_ids"].split(self.pk_separate_by)

        return get_objects_or_404(self.model, pk__in=ids)


class MultipleFormMixin(object):
    """ Mixin provides multiple form handling in class base view. 

        Mix it with FormView to handle multiple forms as a single group. 
        Group may consist of any number of Forms, ModelForms, FormSets and 
        ModelFormSets. Group members are easly avalible through dotted convention.

        Note: handle validated data in your own form_valid method. Group 
            is treated like a single form which means has its own is_valid method.

        Attributes:
            forms (list): List with tuples. Describe all forms included in group
                (order preserved). Each tuple contains form class and it's label 
                (prefix). Prefix consist of name-part and number separated by hyphen.

            formgroup_context_name (str, additional argument): Specify form variable name to use in 
                template instead of 'form'.
    """

    def __init__(self, forms=None, formgroup_context_name=None):
        if forms and formgroup_context_name:
            self.forms = forms
            self.formgroup_context_name = formgroup_context_name

    def get_form_class(self, forms=None):
        """ Create FormGroup instance using django-rebar's formgroup_factory.

            Args:
                forms (list): use instead of self.forms   
        """
        try:
            return formgroup_factory(*[forms or self.forms])
        except NameError:
            raise ImproperlyConfigured(
                "No forms to display. Provide forms attribute.")

    def get_context_data(self, **kwargs):
        """ Replace default form context name.

            Use self.formgroup_context_name if provided. 
        """
        context = super(MultipleFormMixin, self).get_context_data(**kwargs)

        if hasattr(self, "formgroup_context_name"):
            context[self.formgroup_context_name] = context.pop("form")

        return context


class MutableMultipleFormMixin(MultipleFormMixin):
    """ Mixin enhance parent functionality with cloneable forms handling.  

        Some forms from formgroup may be cloneable, which means they can be 
        multiplied and/or reduced using JS (they number may vary).

        Attributes: 
            cloneable_forms (dict): Indicate all forms capable to clone. 
                Keys are name-part of prefixes (look at forms attribute 
                explanation in MultipleFormMixin doc), values are form classes.
    """

    def __init__(self, forms=None, formgroup_context_name=None, cloneable_forms=None):
        if cloneable_forms:
            self.cloneable_forms = cloneable_forms
        super(MutableMultipleFormMixin, self).__init__(
            forms=forms, formgroup_context_name=formgroup_context_name)

    def get_form_class(self):
        """ For any cloneable form call method to update self.forms.

            For any name-part prefix (subprefix) in cloneable_forms call special
            method which checks if form has been clonned and updates self.forms.              
        """

        # If POST update self.forms. Iterate over subprefixes and each time pass
        # all required data to self.update_list_of_tuples.
        if self.request.method == "POST":
            self.list_of_tuples = list(self.forms)
            POST_data = self.request.POST
            cloneable_forms = self.cloneable_forms

            for subprefix, form_class in cloneable_forms.iteritems():
                self.update_list_of_tuples(
                    # list_of_tuples=list_of_tuples,
                    POST_data=POST_data,
                    subprefix=subprefix,
                    form_class=form_class
                )

            return super(MutableMultipleFormMixin, self).get_form_class(forms=self.list_of_tuples)

        # if GET call superclass method
        else:
            return super(MutableMultipleFormMixin, self).get_form_class()

    def update_list_of_tuples(self, POST_data, subprefix, form_class):
        """ Update single cloneable form in self.forms. 

            Call several methods in sequence and pass them appriopriate data. 

            Args:
                list_of_tuples (list): copy of self.forms
                POST_data (dict): copy of request.POST dict
                subprefix (str): name-part of form prefix
        """
        list_of_tuples = self.list_of_tuples
        min_index = self.find_index(subprefix, list_of_tuples)
        max_index = self.find_index(subprefix, list_of_tuples, max=True)
        prefix_patt = self.create_prefix_pattern(subprefix)
        prefixes = self.find_prefixes_in_POST(prefix_patt, POST_data)
        prefixes = self.get_uniqe(prefixes)
        prefixes = self.get_sorted(prefixes)
        list_to_paste = self.prepare_list_to_paste(prefixes, form_class)
        self.replace_sublist_by_list(
            min_index, max_index, self.list_of_tuples, list_to_paste)

        # return mod_list_of_tuples

    @staticmethod
    def find_index(snippet, list_of_tuples, max=False):
        """ Search for tuple in list of tuples using snippet str. 

            Search base on second tuple element. Return first/last 
            occurence.  

            Args:
                snippet (str)
                list_of_tuples (list): list with 2 element tuples
                max (bool): indicate whether return first/last occurence.

            Examples:
                >>> x = [("dog", "A-12"), ("cat", "A-13"), ("horse", "B-10")]
                >>> find_index("A", x)
                0
                >>> find_index("A", x, max=True)
                1     
        """

        lst = list_of_tuples
        if max:
            lst = reversed(lst)
        for i, e in enumerate(lst):
            if snippet in e[1]:
                return i

    @staticmethod
    def replace_sublist_by_list(min_idx, max_idx, lst, list_to_paste):
        """ Replace slice from list using list_to_paste

            Args:
                min_idx (int): slice start index
                max_idx (int): slice end index
                lst (list): list to slice
                list_to_paste (list) 
        """
        lst[min_idx:max_idx] = list_to_paste

    @staticmethod
    def create_prefix_pattern(subprefix):
        """ Create pattern to search through POST keys.

            Args:
                subprefix (str): subprefix (str): name-part of form prefix
        """
        pattern = "{}-\d+".format(subprefix)
        return pattern

    @staticmethod
    def find_prefixes_in_POST(prefix_patt, POST_data):
        """ Get input names from POST keys using prefix pattern. 

            Return keys from POST data that match to prefix pattern str.

            Args:
                prefix_patt (str)
                POST_data (dict)
        """
        prefixes = list()
        for key in POST_data.keys():
            prefix = re.search(prefix_patt, key)
            if prefix:
                prefixes.append(prefix.group())
        return prefixes

    @staticmethod
    def get_uniqe(lst):
        return set(lst)

    @staticmethod
    def get_sorted(lst):
        return sorted(lst)

    @staticmethod
    def prepare_list_to_paste(prefixes, form_class):
        """ Prepare list of tuples to paste into old formgroup list of tuples.

            Args:
                prefixes (list): each of prefix in prefixes will be placed in 
                    separate tuple 
                form_class (specific form class object): object will be placed
                    in each tuple 
        """
        list_to_paste = [(form_class, e) for e in prefixes]
        return list_to_paste
