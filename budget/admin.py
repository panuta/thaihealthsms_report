from django.contrib import admin
from budget.models import *

class BudgetScheduleAdmin(admin.ModelAdmin):
    pass

admin.site.register(BudgetSchedule, BudgetScheduleAdmin)
