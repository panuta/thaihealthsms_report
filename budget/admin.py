from django.contrib import admin
from accounts.models import *

class BudgetScheduleAdmin(admin.ModelAdmin):
    pass

admin.site.register(BudgetSchedule, BudgetScheduleAdmin)
