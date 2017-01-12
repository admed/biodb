from django.conf.urls import url
from views import ProjectListView, RObjectListView, ProjectUpdateView, RObjectDeleteView

app_name = "projects"
urlpatterns = [
    url(r'^$', ProjectListView.as_view(), name="project_list"),
    url(r'^(?P<project_name>\w+)/$', RObjectListView.as_view(), name="robject_list"),
    url(r"^(?P<project_name>\w+)/(?P<robject_ids>(\d+\+)+\d+)/delete/$", RObjectDeleteView.as_view(), name="robject_delete"),
    url(r'^(?P<project_name>\w+)/(?P<robject_ids>\d+)/delete/$', RObjectDeleteView.as_view(), name="robject_delete"),
    url(r'^(?P<pk>[0-9]{1,3})/edit/$',
        ProjectUpdateView.as_view(), name="project_update")
]
