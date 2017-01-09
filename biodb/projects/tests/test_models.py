from django.test import TestCase
from projects.models import Project, RObject, Name
from freezegun import freeze_time 
# from django.core.urlresolvers import reverse
# from guardian.shortcuts import has_


@freeze_time("2001-01-31") # set and stop the clock
class ProjectsModelsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(ProjectsModelsTests, cls).setUpClass()
        # create models instances
        cls.project = Project.objects.create(name="testing_project")
        # robject without Name (id=1)
        cls.robject_noname = RObject.objects.create(author="Piotr Nowak")
        # robject with Name (id=2)
        cls.robject_name = RObject.objects.create(author="Piotr Nowak")
        Name.objects.create(title="C3P0", primary=True,
                            robject=cls.robject_name)

    def test_Project__str__method(self):
        self.assertEqual(str(self.project), "testing_project")

    def test_RObject_get_search_fields_method(self):
        fields = self.robject_noname.get_search_fields()
        self.assertEqual(fields, ["pk", "name", "author"])

    def test_RObject_name_method(self):
        noname = "noname robject, created at 2001-01-31, by Piotr Nowak"
        self.assertEqual(self.robject_noname.name, noname)
        self.assertEqual(self.robject_name.name, "C3P0")


