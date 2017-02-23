from django.test import TestCase
from biodb.mixins import ProjectPermissionMixin, SearchMixin
from biodb import mixins
from projects.models import Project, RObject
from datetime import date
from django.http import Http404
import mock
from mock import call
import copy
from rebar.group import FormGroup
from biodb.mixins import MutableMultipleFormMixin


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
                    "robject_ids": robject_ids
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
            queryset = mixins.DeleteMultipleMixin.get_object(
                self.View("4+5+6"))


# FIXME: thise test case could be written
class MultipleFormMixinTests(TestCase):
                                        # more elegantly, possible using mock
    def setUp(self):
        from django.forms import Form

        # create view imitation
        class FakeViewParent():
            forms = [(Form, "form1"), (Form, "form2")]

            def get_context_data(self):
                return {"form": "value"}

        class FakeViewChild(FakeViewParent):
            formgroup_context_name = "formgroup"

        # copy mixins.MultipleFormClass
        self.MFC = copy.copy(mixins.MultipleFormMixin)
        self.FakeViewParent, self.FakeViewChild = FakeViewParent, FakeViewChild

    def test_get_context_data(self):

        # update base class tuple
        self.MFC.__bases__ = (object, self.FakeViewParent)

        # call get_context_data
        context = self.MFC().get_context_data()

        self.assertEqual(context, {"form": "value"})

        # update base class tuple
        self.MFC.__bases__ = (self.FakeViewChild, object)

        # call get_context_data
        context = self.MFC().get_context_data()

        self.assertEqual(context, {"formgroup": "value"})

    def test_get_form_class(self):

        # update base class tuple
        self.MFC.__bases__ = (object, self.FakeViewParent)

        # get form_class using get_form_class method
        FormClass = self.MFC().get_form_class()

        self.assertTrue(FormClass, FormGroup)
        self.assertTrue(FormClass.form_classes, self.MFC.forms)


class MutableMultipleFormMixinTests(TestCase):

    @mock.patch('biodb.mixins.MutableMultipleFormMixin.handle_post')
    @mock.patch('biodb.mixins.MultipleFormMixin.get_form_class')
    def test_get_form_class(self, method_called_if_get, method_called_if_post):
        m = MutableMultipleFormMixin()

        m.request = mock.Mock()
        m.request.method = "GET"
        m.get_form_class()
        self.assertEqual(method_called_if_get.mock_calls, [call()])

        m.request.method = "POST"
        m.get_form_class()
        self.assertEqual(method_called_if_post.mock_calls, [call()])

    @mock.patch('biodb.mixins.MultipleFormMixin.get_form_class')
    @mock.patch('biodb.mixins.MutableMultipleFormMixin.update_list_of_tuples_attr')
    def test_handle_post(self, update_list_of_tuples_attr, super_get_form_class):
        update_list_of_tuples_attr.return_value = "mod_list_of_tuples"

        m = MutableMultipleFormMixin()
        m.forms = [("class1", "prefixA-1"), ("class1",
                                             "prefixA-2"), ("class2", "prefixB")]
        m.request = mock.Mock()
        m.request.POST = {"prefixA-1": "dog",
                          "prefixA-3": "cat", "prefixB": "horse"}
        m.cloneable_forms = [("class1", "prefixA")]

        m.handle_post()

        self.assertEqual(update_list_of_tuples_attr.mock_calls, [call(
                list_of_tuples = m.forms,
                POST_data=m.request.POST,
                subprefix="prefixA",
                form_class="class1"
            )])

        self.assertEqual(super_get_form_class.mock_calls, [call(
            forms="mod_list_of_tuples")])

    @mock.patch.multiple("biodb.mixins.MutableMultipleFormMixin",
                         find_index=mock.MagicMock(side_effect=[0, 10]),
                         create_prefix_pattern=mock.MagicMock(
                             return_value="pattern"),
                         find_prefixes_in_POST=mock.MagicMock(
                             return_value="prefixes"),
                         get_uniqe=mock.MagicMock(
                             return_value="uniqe_prefixes"),
                         get_sorted=mock.MagicMock(
                             return_value="sort_prefixes"),
                         prepare_list_to_paste=mock.MagicMock(
                             return_value="list_to_paste"),
                         replace_sublist_by_list=mock.MagicMock(
                             return_value="mod_list_of_tuples")
                         )
    def test_update_list_of_tuples_attr(self, **kwargs):
        m = MutableMultipleFormMixin()

        # m.list_of_tuples = "list_of_tuples"

        mod_list_of_tuples = m.update_list_of_tuples_attr(
            list_of_tuples="list_of_tuples",
            POST_data="data",
            subprefix="prefix",
            form_class="form_class"
        )

        self.assertEqual(m.find_index.mock_calls, [call(
            'prefix', 'list_of_tuples'), call('prefix', 'list_of_tuples', max=True)])
        self.assertEqual(m.create_prefix_pattern.mock_calls, [call("prefix")])
        self.assertEqual(m.find_prefixes_in_POST.mock_calls,
                         [call("pattern", "data")])
        self.assertEqual(m.get_uniqe.mock_calls, [call("prefixes")])
        self.assertEqual(m.get_sorted.mock_calls, [call("uniqe_prefixes")])
        self.assertEqual(m.prepare_list_to_paste.mock_calls, [
                         call("sort_prefixes", "form_class")])
        self.assertEqual(m.replace_sublist_by_list.mock_calls, [
                         call(0, 11, 'list_of_tuples', 'list_to_paste')])
        self.assertEqual(mod_list_of_tuples, "mod_list_of_tuples")

    def test_find_index(self):
        m = MutableMultipleFormMixin()
        list_of_tuples = [("1", "Aa"), ("2", "Aa"), ("3", "Aa"), ("4", "Bb")]
        min_index = m.find_index("A", list_of_tuples)
        max_index = m.find_index("A", list_of_tuples, max=True)
        self.assertEqual(min_index, 0)
        self.assertEqual(max_index, 2)

    def test_replace_sublist_by_list(self):
        lst = ["A", "B", "C", "D"]
        list_to_paste = ["1", "2"]
        m = MutableMultipleFormMixin()
        new_lst = m.replace_sublist_by_list(1, 2, lst, list_to_paste)
        self.assertEqual(new_lst, ["A", "1", "2", "C", "D"])

    def test_create_prefix_pattern(self):
        m = MutableMultipleFormMixin()
        pattern = m.create_prefix_pattern(subprefix="prefix")
        self.assertEqual(pattern, "prefix-\d+")

    def test_find_prefixes_in_POST(self):
        data = {"adult-1": "Joey", "adult-2": "Chandler", "child-1": "Ross"}
        m = MutableMultipleFormMixin()
        keys = m.find_prefixes_in_POST("adult-\d+", data)

        self.assertEqual(keys, ["adult-1", "adult-2"])

    def test_prepare_list_to_paste(self):
        m = MutableMultipleFormMixin()
        form_class = mock.MagicMock
        lot = m.prepare_list_to_paste(
            ["name-1", "name-2", "name-3"], form_class)
        self.assertEqual(lot, [(form_class, "name-1"),
                               (form_class, "name-2"), (form_class, "name-3")])
