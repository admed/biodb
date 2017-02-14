from django.shortcuts import get_object_or_404
from patches.shortcuts import get_objects_or_404
from projects.models import Project
from watson import search as watson
from rebar.group import formgroup_factory
from django.views import generic
import re
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
    """
       Mix it with FormView to handle multiple forms as a single group.
       Requires:
       - **forms** attribute: list of tuples '(form_class, form_prefix)' 
       you want to use in group.
       - your own form_valid() method      

    """

    def get_form_class(self, forms=None):
        """
            Create formgroup using django-rebar. 
        """

        # print self.forms
        # print forms
        return formgroup_factory(*[forms or self.forms])

    def get_context_data(self, **kwargs):
        """
            Replace default form context name with self.formgroup_context_name.
        """
        
        context = super(MultipleFormMixin, self).get_context_data(**kwargs)
        context[self.formgroup_context_name] = context.pop("form")
        return context


class MutableMultipleFormMixin(MultipleFormMixin):
    """
       Mix it with FormView to handle multiple view as a single group. 
       However some forms may be cloneable, which means they can be 
       multiplied and/or reduced using JS.

       Requires:
       - **forms** attribute: list of tuples '(form_class, form_prefix)' 
       you want to use in group.
       - your own form_valid() method      
    """

    def get_form_class(self):
        """
            Create and return FormGroup subclass depending on the request.method.  
        """
        # if POST method, update self.forms
        # self.forms must be list of tuples (form_class, "prefix")
        if self.request.method == "POST":
            data = self.request.POST
            forms = list(self.forms) # REMEMBER: do not modify self.forms, becouse it's 
            # cached somewhere 

            for corePrefix, form_class in self.cloneable_forms.iteritems():
                # get forms full prefixes from POST using corePrefix
                fullPrefixes = self.get_forms_prefixes(data, corePrefix)
                print "fullPrefixes: {}".format(fullPrefixes)
                # bulild list of tuples to replace in self.forms
                newTuples = [(form_class, prefix) for prefix in fullPrefixes]
                # update self.forms
                self.update_forms(listOfTuples=forms,
                                 toPaste=newTuples, cutTupleWith=corePrefix)

            return super(MutableMultipleFormMixin, self).get_form_class(forms=forms)

        # if GET call superclass method
        else:
            return super(MutableMultipleFormMixin, self).get_form_class()

    def get_forms_prefixes(self, data, prefix):
        """
            Extract given form id's from POST data using prefix.
        """
        # container for id's strings
        ids = list()
        # create a pattern to search
        pattern = "{}-\d+".format(prefix)

        for key in data.keys():
            # match to pattern
            id = re.search(pattern, key)
            # if matched
            if id:
                ids.append(id.group())
        # get uniqe 
        ids = set(ids)
        # sort aphabetically
        return sorted(ids)

    @staticmethod
    def update_forms(listOfTuples, toPaste, cutTupleWith):
        # find id of tuples to cut 
        idxs = [i for i in range(len(listOfTuples))
                if cutTupleWith in listOfTuples[i][1]]
        print "idxs: {}".format(idxs) 
        # replace old tuples with new ones
        listOfTuples[min(idxs):max(idxs) + 1] = toPaste
        print toPaste
        # reuturn new list of tuples
        # return listOfTuples
