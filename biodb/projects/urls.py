from django.conf.urls import url
import views

app_name = "projects"
urlpatterns = [
    # Project URLs
    url(r'^$', views.ProjectListView.as_view(), name="project_list"),
    url(r'^(?P<pk>[0-9]{1,3})/edit/$',
        views.ProjectUpdateView.as_view(), name="project_update"), 
    # RObject URLs
    url(r'^(?P<project_name>\w+)/$', views.RObjectListView.as_view(), name="robject_list"),
    url(r"^(?P<project_name>\w+)/(?P<robject_ids>(\d+\+)+\d+)/delete/$", views.RObjectDeleteView.as_view(), name="robject_delete"),
    url(r'^(?P<project_name>\w+)/(?P<robject_ids>\d+)/delete/$', views.RObjectDeleteView.as_view(), name="robject_delete"),
    url(r'^(?P<project_name>\w+)/create/(?P<number_of_name_forms>[1-9]\d*)/$', views.RObjectCreateView.as_view(), name="robject_create"),
    url(r'^(?P<project_name>\w+)/(?P<pk>[0-9]+)/details/$', views.RObjectDetailView.as_view(), name="robject_detail"),
    # url(r'^(?P<project_name>\w+)/(?P<pk>[0-9]+)/edit/$', RObjectUpdate.as_view(), name='robject_edit'),
    
]
