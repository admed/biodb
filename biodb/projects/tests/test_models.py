from django.test import TestCase
from projects.models import Project
# from django.core.urlresolvers import reverse
# from guardian.shortcuts import has_


class ProjectsModelsTests(TestCase):
    
    @classmethod
    def setUpClass(cls):
        super(ProjectsModelsTests, cls).setUpClass()
        # create models instances
        cls.project = Project.objects.create(name="testing_project")

    def test_Project__str__method(self):
        self.assertEqual(str(self.project), "testing_project")