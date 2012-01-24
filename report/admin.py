from django.contrib import admin
from report.models import *

class ReportAdmin(admin.ModelAdmin):
    pass

class ReportAssignmentAdmin(admin.ModelAdmin):
    pass

class ReportSubmissionAdmin(admin.ModelAdmin):
    pass

class ReportSubmissionAttachmentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Report, ReportAdmin)
admin.site.register(ReportAssignment, ReportAssignmentAdmin)
admin.site.register(ReportSubmission, ReportSubmissionAdmin)
admin.site.register(ReportSubmissionAttachment, ReportSubmissionAttachmentAdmin)
