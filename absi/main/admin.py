from django.contrib import admin
from pagetree.models import Hierarchy, Section
from absi.main.models import UserProfile


admin.site.register(Hierarchy)
admin.site.register(Section)
admin.site.register(UserProfile)
