from django.conf.urls import url
from views import ProjectListView, RObjectListView, RObjectDeleteView, RObjectCreateView

app_name = "projects"
urlpatterns = [
    url(r'^$', ProjectListView.as_view(), name="project_list"),
    url(r'^(?P<project_name>\w+)/$', RObjectListView.as_view(), name="robject_list"),
    url(r"^(?P<project_name>\w+)/(?P<robject_ids>(\d+\+)+\d+)/delete/$", RObjectDeleteView.as_view(), name="robject_delete"),
    url(r'^(?P<project_name>\w+)/(?P<robject_ids>\d+)/delete/$', RObjectDeleteView.as_view(), name="robject_delete"),
    url(r'^(?P<project_name>\w+)/create/(?P<number_of_name_forms>[1-9]\d*)/$', RObjectCreateView.as_view(), name="robject_create"),
]
