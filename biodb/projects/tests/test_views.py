from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission
# from django.contrib.auth
from projects.models import Project, RObject, Name
from django.core.urlresolvers import reverse
from guardian.shortcuts import assign_perm
from projects import views
from django.forms.models import ModelForm
from django.forms.formsets import BaseFormSet
from projects.forms import BaseNameFormSet
import datetime


# TODO: consider if this superclass is a good idea (slow speed down)
class ProjectsViewsTests(TestCase):
    ''' Superclass for every test class in this module '''

    @classmethod
    def setUpClass(cls):
        ''' Called once when test class is set up. Provide all basic requirements to inteact 
        with views: create user, activate user, log client in, create project, attach project 
        permission to user.  '''

        super(ProjectsViewsTests, cls).setUpClass()

        # create user
        cls.user = User.objects.create_user(
            username="john", password="johnpassword")

        # activate
        cls.user.is_active = True

        # log client in
        cls.c = Client()
        cls.c.login(username="john", password="johnpassword")

        # create projects
        cls.project = Project.objects.create(name="test_project")

        # add permissions
        permission1 = Permission.objects.get(codename='can_visit_project')
        permission2 = Permission.objects.get(codename='can_modify_project_content')
        cls.user.user_permissions.add(permission1, permission2)

        # assign permission to project instance
        assign_perm("can_visit_project", cls.user, cls.project)
        assign_perm('can_modify_project_content', cls.user, cls.project)


class ProjectListViewTests(ProjectsViewsTests):

    def test_ProjectListView(self):

        resp = self.c.get(reverse("projects:project_list"))

        self.assertTemplateUsed(resp, 'projects/project_list.html')
        self.assertEqual(resp.status_code, 200)


class RObjectListViewTests(ProjectsViewsTests):
    @classmethod
    def setUpClass(cls):
        ''' Extend super setUpClass '''

        super(RObjectListViewTests, cls).setUpClass()

        # create robjects (2 related to project, 1 unrelated)
        cls.robject_1 = RObject.objects.create(
            project=cls.project, create_date=datetime.date(2010, 10, 20))
        cls.robject_2 = RObject.objects.create(
            project=cls.project, create_date=datetime.date(2000, 01, 10))
        cls.robject_3 = RObject.objects.create()

        # create robjects names
        Name.objects.create(title="robject_1", primary=True,
                            robject=cls.robject_1)
        Name.objects.create(title="robject_2", primary=True,
                            robject=cls.robject_2)
        Name.objects.create(title="robject_3", primary=True,
                            robject=cls.robject_3)

    def test_get_table_data_method(self):
        # test get request (get_table_data method)
        resp = self.c.get(reverse("projects:robject_list",
                                  kwargs={"project_name": "test_project"}))

        self.assertIn(self.robject_1, resp.context["table"].data)
        self.assertIn(self.robject_2, resp.context["table"].data)
        self.assertNotIn(self.robject_3, resp.context["table"].data)
        self.assertTemplateUsed(resp, 'projects/robject_list.html')
        self.assertEqual(resp.status_code, 200)

    def test_get_form_valid_method(self):
        # test if form_valid render proper template, create new form instace and calls get_table_data()
        # test if get_table_data() calls SearchMixin.search() and
        # SearchMixin.filter() methods
        resp = self.c.post(reverse("projects:robject_list",
                                   kwargs={"project_name": "test_project"}),
                           data={"query": "robject", "after_date": "2010-01-01", "before_date": ""})

        self.assertIn(self.robject_1, resp.context["table"].data)
        self.assertEqual(len(resp.context["table"].data), 1)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'projects/robject_list.html')
        self.assertFalse(resp.context["form"].is_bound)

    def test_post_method(self):
        """
            Test if post method redirect user when specific POST data is passed, 
            and where this redirect leads. 
        """
        POST_data = {
            "actions-form": False,
            "csrfmiddlewaretoken": None, # include token imitation
            "1": "checked",
            "101": "checked"
        }

        resp = self.c.post(reverse("projects:robject_list", kwargs={
                           "project_name": "test_project"}), data=POST_data)
        self.assertRedirects(resp, reverse("projects:robject_delete", kwargs={
                             "project_name": "test_project", "robject_ids": "1+101"}))

class RObjectCreateViewTests(ProjectsViewsTests):
    @classmethod
    def setUpClass(cls):
        super(RObjectCreateViewTests, cls).setUpClass()

        cls.view = views.RObjectCreateView(kwargs = {"number_of_name_forms":1})

    def test_get_form_class_method(self): # test without client
        # create form_class using method
        form_class = self.view.get_form_class()

        # check if it's FormGroup class
        self.assertEqual(form_class.__name__, "FormGroup")

        # check if contains two forms
        form_subclasses = form_class.form_classes  
        self.assertEqual(len(form_subclasses), 2)

        # unpack FormGroup and test single forms
        form_set = form_subclasses[0][0]
        model_form = form_subclasses[1][0]
        self.assertTrue(issubclass(form_set, BaseNameFormSet))  
        self.assertTrue(issubclass(model_form, ModelForm))

        # test formset:

        # test model
        self.assertEqual(form_set.model, Name)
        # test number of forms in formset
        self.assertEqual(form_set.extra, self.view.kwargs["number_of_name_forms"]) 
        # test fields exclude
        self.assertEqual(("robject",), form_set.form.Meta.exclude) 

        # test model_form:

        # test model
        self.assertEqual(model_form.Meta.model, RObject)
        # test fields exclude
        self.assertEqual(("project","creator",), model_form.Meta.exclude) 

    # TODO: finish testing this view after modernization!


    # def test_RobjectDetailView(self):
    #     pass

    # def test_RobjectCreateView(self):
    #     pass

    # def test_RobjectDeleteView(self):
    #     pass

    # def test_BioObjCreateView(self):
    #     pass

    # def test_BioObjUpdateView(self):
    #     pass

    # def test_BioObjDeleteView(self):
    #     pass
