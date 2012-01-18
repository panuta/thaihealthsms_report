from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    firstname = models.CharField(max_length=300)
    lastname = models.CharField(max_length=300)
    random_password = models.CharField(max_length=30, null=True)

    def get_fullname(self):
        return '%s %s' % (self.firstname, self.lastname)

class UserSector(models.Model):
    user = models.ForeignKey(User)
    sector = models.ForeignKey('domain.Sector')

class ProjectResponsibility(models.Model): # for sector cordinator
    user = models.ForeignKey(User)
    project = models.ForeignKey('domain.Project')

class ProjectManager(models.Model): # for project manager
    user = models.ForeignKey(User)
    project = models.ForeignKey('domain.Project')

