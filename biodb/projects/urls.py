from django.conf.urls import url
from views import ProjectListView, RObjectListView, ProjectUpdateView

app_name = "projects"
urlpatterns = [
    url(r'^$', ProjectListView.as_view(), name="project_list"),
    url(r'^(?P<project_name>\w+)/$', RObjectListView.as_view(), name = "project_detail"),
    url(r'^(?P<pk>[0-9]{1,3})/edit/$', ProjectUpdateView.as_view(), name="project_update")
]