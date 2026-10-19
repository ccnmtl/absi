from django.contrib import admin
from pagetree.models import Hierarchy, Section, UserPageVisit
from absi.main.models import UserProfile


admin.site.register(Hierarchy)
admin.site.register(Section)
admin.site.register(UserPageVisit)
admin.site.register(UserProfile)
