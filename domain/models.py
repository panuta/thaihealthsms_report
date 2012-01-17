from django.db import models

class Sector(models.Model):
    ref_no = models.IntegerField()
    name = models.CharField(max_length=500)

class MasterPlan(models.Model):
    ref_no = models.IntegerField()
    name = models.CharField(max_length=500)

class SectorMasterPlan(models.Model):
    sector = models.ForeignKey(Sector)
    master_plan = models.ForeignKey(MasterPlan)

class Project(models.Model):
    master_plan = models.ForeignKey(MasterPlan)
    ref_no = models.CharField(max_length=100, unique=True)
    contract_no = models.CharField(max_length=100, null=True, unique=True)
    name = models.CharField(max_length=1000)
    abbr_name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    manager_name = models.CharField(max_length=300, blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    project_type = models.IntegerField(default=0) # Not use yet
    status = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('accounts.UserProfile')

    class Meta:
        ordering = ['ref_no']
