from django.db import models

class BudgetSchedule(models.Model):
    project = models.ForeignKey('domain.Project')
    cycle = models.IntegerField()
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    due_date = models.DateField(null=True)
    grant_budget = models.IntegerField(default=0)
    claim_budget = models.IntegerField(default=0)
    claimed_on = models.DateField(null=True)
    