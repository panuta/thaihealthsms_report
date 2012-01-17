from django.db import models

class BudgetSchedule(models.Model):
    project = models.ForeignKey('domain.Project')
    grant_budget = models.IntegerField(default=0)
    claim_budget = models.IntegerField(default=0)
    schedule_on = models.DateField()
    claimed_on = models.DateField(null=True)
    remark = models.CharField(max_length=1000, blank=True)