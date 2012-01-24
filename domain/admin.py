from django.contrib import admin
from domain.models import *

class SectionAdmin(admin.ModelAdmin):
    pass

class ProjectAdmin(admin.ModelAdmin):
    pass

class ImportGMSAdmin(admin.ModelAdmin):
    pass

class ImportGMSProjectsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Section, SectionAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ImportGMS, ImportGMSAdmin)
admin.site.register(ImportGMSProjects, ImportGMSProjectsAdmin)
