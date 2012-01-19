from django.contrib.auth.models import User, Group
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    firstname = models.CharField(max_length=300)
    lastname = models.CharField(max_length=300)
    random_password = models.CharField(max_length=30, null=True)
    primary_role = models.ForeignKey(Group)

    def get_fullname(self):
        return '%s %s' % (self.firstname, self.lastname)

class UserSection(models.Model):
    user = models.ForeignKey(User)
    section = models.ForeignKey('domain.Section')

class ProjectResponsibility(models.Model): # for section cordinator
    user = models.ForeignKey(User)
    project = models.ForeignKey('domain.Project')

class ProjectManager(models.Model): # for project manager
    user = models.ForeignKey(User)
    project = models.ForeignKey('domain.Project')

