from django.contrib import admin
from models import Project, RObject
from guardian.admin import GuardedModelAdmin

# Register your models here.
admin.site.register(Project, GuardedModelAdmin)
admin.site.register(RObject, GuardedModelAdmin)