from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission
# from django.contrib.auth
from projects.models import Project, RObject, Name
from django.core.urlresolvers import reverse
from guardian.shortcuts import assign_perm
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
        permission = Permission.objects.get(codename='can_visit_project')
        cls.user.user_permissions.add(permission)

        # assign permission to project instance
        assign_perm("can_visit_project", cls.user, cls.project)


class ProjectListViewTests(ProjectsViewsTests):

    def test_ProjectListView(self):

        resp = self.c.get(reverse("projects:project_list"))

        self.assertTemplateUsed(resp, 'projects/project_list.html')
        self.assertEqual(resp.status_code, 200)


class RObjectListView(ProjectsViewsTests):
    @classmethod
    def setUpClass(cls):
        ''' Extend super setUpClass '''

        super(RObjectListView, cls).setUpClass()

        # create robjects (2 related to project, 1 unrelated)
        cls.robject_1 = RObject.objects.create(project=cls.project, create_date=datetime.date(2010, 10, 20))
        cls.robject_2 = RObject.objects.create(project=cls.project, create_date=datetime.date(2000, 01, 10))
        cls.robject_3 = RObject.objects.create()

        # create robjects names
        Name.objects.create(title="robject_1", primary=True,
                            robject=cls.robject_1)
        Name.objects.create(title="robject_2", primary=True,
                            robject=cls.robject_2)
        Name.objects.create(title="robject_3", primary=True,
                            robject=cls.robject_3)

    def test_RObjectListView(self):
        # test get request (get_table_data method)
        resp = self.c.get(reverse("projects:project_detail",
                                  kwargs={"project_name": "test_project"}))

        self.assertIn(self.robject_1, resp.context["table"].data)
        self.assertIn(self.robject_2, resp.context["table"].data)
        self.assertNotIn(self.robject_3, resp.context["table"].data)
        self.assertTemplateUsed(resp, 'projects/robject_list.html')
        self.assertEqual(resp.status_code, 200)

        # test post request

        # test if form_valid render proper template, create new form instace and calls get_table_data()
        # test if get_table_data() calls SearchMixin.search() and SearchMixin.filter() methods
        resp = self.c.post(reverse("projects:project_detail", 
                           kwargs={"project_name": "test_project"}), 
                           data={"query": "robject", "after_date": "2010-01-01", "before_date": ""})

        self.assertIn(self.robject_1, resp.context["table"].data)
        self.assertEqual(len(resp.context["table"].data), 1)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'projects/robject_list.html')
        self.assertFalse(resp.context["form"].is_bound)


    # def test_RobjectDetailView(self):
    #     pass

    # def test_RobjectCreateView(self):
    #     pass

    # def test_RobjectUpdateView(self):
    #     pass

    # def test_RobjectDeleteView(self):
    #     pass

    # def test_BioObjCreateView(self):
    #     pass

    # def test_BioObjUpdateView(self):
    #     pass

    # def test_BioObjDeleteView(self):
    #     pass
