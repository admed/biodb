from django.test import TestCase
from biodb.mixins import ProjectPermissionMixin, SearchMixin
from biodb import mixins
from projects.models import Project, RObject
from datetime import date
from django.http import Http404


class ProjectPermissionMixinTests(TestCase):
    @classmethod
    def setUpClass(cls):
        ''' Provide imitation of view instance with kwargs attribute + create project '''

        super(ProjectPermissionMixinTests, cls).setUpClass()

        # view must inherit from ProjectPermissionMixin (otherwise an error
        # occurs!)
        class View(ProjectPermissionMixin):
            ''' View imitation class '''

            def __init__(self, kwargs):
                self.kwargs = kwargs  # its dict

        # create instance
        cls.view = View(kwargs={"project_name": "project_test"})

        # create project
        cls.project = Project.objects.create(name="project_test")

    def test_get_permission_object_method(self):
        # test the logic of this method
        project = ProjectPermissionMixin.get_permission_object(self.view)
        self.assertEqual(project, self.project)


class SearchMixinTests(TestCase):
    @classmethod
    def setUpClass(cls):
        ''' Create couple projects '''
        super(SearchMixinTests, cls).setUpClass()

        cls.project_1 = Project.objects.create(
            name="project_1", create_date=date(2001, 01, 01))
        cls.project_2 = Project.objects.create(
            name="project_2", create_date=date(2002, 01, 01))
        cls.project_3 = Project.objects.create(
            name="project_3", create_date=date(2003, 01, 01))

    def test_search_method(self):
        # search method has no logic (only pass arguments to different method)
        pass

    def test_filter_method(self):
        ''' Test the way method decides which arguments pass to manager's 
        filter method and what keywords use'''

        # after date only
        queryset = SearchMixin.filter(
            Project.objects.all(), after="2001-01-02", before="")

        self.assertNotIn(self.project_1, queryset)
        self.assertIn(self.project_2, queryset)
        self.assertIn(self.project_3, queryset)

        # after and before dates
        queryset = SearchMixin.filter(
            Project.objects.all(), after="2001-01-02", before="2002-12-31")

        self.assertNotIn(self.project_1, queryset)
        self.assertIn(self.project_2, queryset)
        self.assertNotIn(self.project_3, queryset)

        # before date only
        queryset = SearchMixin.filter(
            Project.objects.all(), after="", before="2002-12-31")

        self.assertIn(self.project_1, queryset)
        self.assertIn(self.project_2, queryset)
        self.assertNotIn(self.project_3, queryset)

        # gte keyword
        queryset = SearchMixin.filter(
            Project.objects.all(), after="2001-01-01", before="")

        self.assertIn(self.project_1, queryset)

        # lte keyword
        queryset = SearchMixin.filter(
            Project.objects.all(), after="", before="2003-01-01")

        self.assertIn(self.project_3, queryset)


class DeleteMultipleMixinTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(DeleteMultipleMixinTests, cls).setUpClass()

        # create imitation of view with kwargs and model attributes

        class View(mixins.DeleteMultipleMixin):
            model = RObject

            def __init__(self, robject_ids):
                self.kwargs = {
                    "robject_ids" : robject_ids 
                }

        cls.View = View

        # create robjects
        cls.robject1 = RObject.objects.create()
        cls.robject2 = RObject.objects.create()
        cls.robject3 = RObject.objects.create()

    def test_get_object_method(self):

        # query existing robjects
        queryset = mixins.DeleteMultipleMixin.get_object(self.View("1+2+3"))

        self.assertIn(self.robject1, queryset)
        self.assertIn(self.robject2, queryset)
        self.assertIn(self.robject3, queryset)

        # query existing with not existing objects
        queryset = mixins.DeleteMultipleMixin.get_object(self.View("1+100+3"))

        self.assertIn(self.robject1, queryset)
        self.assertIn(self.robject3, queryset)
        
        # query not existing robjects
        with self.assertRaisesMessage(Http404, 'No RObject matches the given query.'):
            queryset = mixins.DeleteMultipleMixin.get_object(self.View("4+5+6"))

