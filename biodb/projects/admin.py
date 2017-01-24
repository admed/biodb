from django.contrib import admin
from .models import Project, RObject, Name, Tag
from guardian.admin import GuardedModelAdmin

# Register your models here.
admin.site.register(Project, GuardedModelAdmin)
admin.site.register(RObject, GuardedModelAdmin)
admin.site.register(Name, GuardedModelAdmin)
admin.site.register(Tag, GuardedModelAdmin)