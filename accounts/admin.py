from django.contrib import admin
from accounts.models import *

class RoleAdmin(admin.ModelAdmin):
    pass

class UserProfileAdmin(admin.ModelAdmin):
    pass

class UserSectionAdmin(admin.ModelAdmin):
    pass

class ProjectResponsibilityAdmin(admin.ModelAdmin):
    pass

class ProjectManagerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Role, RoleAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserSection, UserSectionAdmin)
admin.site.register(ProjectResponsibility, ProjectResponsibilityAdmin)
admin.site.register(ProjectManager, ProjectManagerAdmin)
