# -*- encoding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

class Section(models.Model):
    ref_no = models.CharField(max_length=10)
    prefix = models.CharField(max_length=50)
    name = models.CharField(max_length=500)
    long_abbr_name = models.CharField(max_length=100)
    short_abbr_name = models.CharField(max_length=100)
    order_number = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s - %s' % (self.short_abbr_name, self.name)

class Project(models.Model):
    section = models.ForeignKey(Section)
    ref_no = models.CharField(max_length=100, unique=True)
    contract_no = models.CharField(max_length=100, null=True, unique=True)
    prefix = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=1000)
    abbr_name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    manager_name = models.CharField(max_length=300, blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    project_type = models.IntegerField(default=0) # Not use yet
    status = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)

    class Meta:
        ordering = ['ref_no']
    
    def is_active(self):
        return self.status in (u'อนุมัติ', u'รอปิดโครงการ')

## IMPORT FROM GMS ##

class ImportGMS(models.Model):
    started = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField()
    imported_by = models.ForeignKey(User)
    created_projects = models.IntegerField(default=0)
    updated_projects = models.IntegerField(default=0)
    notfound_projects = models.IntegerField(default=0)
    created_budgets = models.IntegerField(default=0)

class ImportGMSProjects(models.Model):
    job = models.ForeignKey(ImportGMS)
    project_ref_no = models.CharField(max_length=100)
    is_found = models.BooleanField()
    is_created = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
