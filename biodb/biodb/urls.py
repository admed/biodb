from django.conf.urls import include, url
from django.contrib import admin

app_name = "biodb"
urlpatterns = [
    # Examples:
    # url(r'^$', 'biodb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^projects/', include('projects.urls', namespace="projects")),
    url(r'^', include('userena.urls'))  
]

