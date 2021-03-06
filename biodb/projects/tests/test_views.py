from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission
# from django.contrib.auth
from projects.models import Project, RObject, Name
from django.core.urlresolvers import reverse
from guardian.shortcuts import assign_perm
import datetime
import mock
from rebar.group import formgroup_factory
from projects import views
from projects.forms import RObjectForm, NameForm


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
        permission2 = Permission.objects.get(
            codename='can_modify_project_content')
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
            "csrfmiddlewaretoken": None,  # include token imitation
            "1": "checked",
            "101": "checked"
        }

        resp = self.c.post(reverse("projects:robject_list", kwargs={
                           "project_name": "test_project"}), data=POST_data)
        self.assertRedirects(resp, reverse("projects:robject_delete", kwargs={
                             "project_name": "test_project", "robject_ids": "1+101"}))


class RObjectCreateViewTests(ProjectsViewsTests):
    @mock.patch("projects.views.redirect", return_value="redirect in progress!")
    def test_form_valid(self, redirect_function):
        Form = mock.Mock
        lot = [(Form, "name1"), (Form, "name2"), (Form, "robject")]
        FormClass = formgroup_factory(*[lot])
        form = FormClass()
        robject, name1, name2 = mock.Mock(
            name="robject"), mock.Mock(), mock.Mock()
        robject.save, name1.save, name2.save = mock.Mock(), mock.Mock(), mock.Mock()
        form.robject.save = mock.Mock(return_value=robject)
        form.name1.save = mock.Mock(return_value=name1)
        form.name2.save = mock.Mock(return_value=name2)

        instance = mock.Mock(spec=views.RObjectCreateView)
        instance.get_success_url = mock.Mock(return_value="success_url")
        result = views.RObjectCreateView.form_valid(instance, form)

        form.robject.save.assert_called_once_with(commit=False)
        form.name1.save.assert_called_once_with(commit=False)
        form.name2.save.assert_called_once_with(commit=False)

        robject.save.assert_called_once_with()
        name1.save.assert_called_once_with()
        name1.save.assert_called_once_with()

        self.assertEqual(name1.robject, robject)
        self.assertEqual(name2.robject, robject)

        instance.get_success_url.assert_called_once_with()
        redirect_function.assert_called_once_with("success_url")
        self.assertEqual(result, "redirect in progress!")

    @mock.patch("projects.views.reverse")
    def test_get_success_url(self, reverse_function):
        instance = mock.Mock(spec=views.RObjectCreateView)
        instance.kwargs = {"project_name": "best_name_ever"}
        views.RObjectCreateView.get_success_url(instance)
        reverse_function.assert_called_once_with("projects:robject_list", kwargs={
                                                 "project_name": "best_name_ever"})

    def test_view(self):
        """ Integration test. 

            Test:
                get method:
                    response status code
                    template used
                    form instance in context
                    form instance name in context
                post method:
                    valid data passed:
                        response status code
                        response redirect address
                        creted robject in db
                    invalid data passed:
                        response status code
                        form errors in template  
        """
        url = reverse("projects:robject_create", kwargs={
            "project_name": "test_project"})

        # GET method
        resp = self.c.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "projects/robject_create.html")

        # prepare form_class to compare
        lst = [(NameForm, "name-1"), (RObjectForm, "robject")]
        FormClass = formgroup_factory(*[lst])
        self.assertEqual(
            resp.context["formgroup"].form_classes, FormClass().form_classes)

        # POST method, valid data
        # pass only those data, which user is allowed to enter in form
        # include onlu required fields
        # (validation depends inter alia on model fields specification)
        data = {
            "group-name-1-title": "hej",  # required field
            "group-robject-project": "1"  # required field
            # ... many other fields ommited
        }
        resp = self.c.post(url, data=data)
        expected_url = reverse("projects:robject_list", kwargs={
                               "project_name": "test_project"})
        self.assertRedirects(resp, expected_url)

        # POST method, invalid data
        data = {
            "group-name-1-title": "",
            "group-robject-project": ""
            # ... many other fields ommited
        }
        resp = self.c.post(url, data=data)
        self.assertEqual(resp.status_code, 200)

        expected_errors = [{'title': [u'This field is required.']}, {
            'project': [u'This field is required.']}]
        # unnecessary assertion but whatever..
        self.assertEqual(resp.context["formgroup"].errors, expected_errors) 

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
