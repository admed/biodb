from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission
# from django.contrib.auth
from projects.models import Project
from django.core.urlresolvers import reverse
from guardian.shortcuts import assign_perm

class ProjectsViewsTests(TestCase):
    
    @classmethod
    def setUpClass(cls):
        ''' Called once in the begining before any tests. '''

        super(ProjectsViewsTests, cls).setUpClass()

        # create user 
        user = User.objects.create_user(username="john", password="johnpassword")

        # activate
        user.is_active = True

        # add permissions
        permission = Permission.objects.get(codename='can_visit')
        user.user_permissions.add(permission)


        # create projects
        test_project = Project.objects.create(name="test_project")

        # assign permission to project instances
        assign_perm("can_visit", user, test_project)

        # log in client 
        cls.c = Client()
        cls.c.login(username="john", password="johnpassword")
    
    def test_ProjectListView(self):

        resp = self.c.get(reverse("projects:project_list"), follow=True)

        
        self.assertTemplateUsed(resp, 'projects/project_list.html')
        self.assertEqual(resp.status_code, 200)

    def test_ProjectDetailView(self):
        resp = self.c.get(reverse("projects:project_detail", kwargs={"slug":"test_project"}))
        
        self.assertTemplateUsed(resp, 'projects/project_detail.html')
        self.assertEqual(resp.status_code, 200)

    def test_RobjectListView(self):
        resp = self.c.get(reverse("projects:robject_list"))

        self.assertTemplateUsed(resp, 'projects/robject_list.html')
        self.assertEqual(resp.status_code, 200) 

    def test_RobjectDetailView(self):
        pass

    def test_RobjectCreateView(self):
        pass

    def test_RobjectUpdateView(self):
        pass

    def test_RobjectDeleteView(self):
        pass

    def test_BioObjCreateView(self):
        pass

    def test_BioObjUpdateView(self):
        pass

    def test_BioObjDeleteView(self):
        pass


