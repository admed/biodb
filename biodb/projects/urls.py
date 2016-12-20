from django.conf.urls import include, url
from views import ProjectsView, ProjectDetailView, ProjectUpdateView

app_name = "projects"
urlpatterns = [
    url(r'^$', ProjectsView.as_view(), name="projects_list"),
    url(r'^(?P<pk>[0-9]{1,3})/$', ProjectDetailView.as_view(), name = "project_detail"),
    url(r'^(?P<pk>[0-9]{1,3})/edit/$', ProjectUpdateView.as_view(), name="project_update")
]