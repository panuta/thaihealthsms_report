from django.contrib.auth.models import User
from django.db import models

class Role(models.Model):
    code = models.CharField(max_length=300, db_index=True, unique=True)
    name = models.CharField(max_length=300)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    firstname = models.CharField(max_length=300)
    lastname = models.CharField(max_length=300)
    random_password = models.CharField(max_length=30, null=True)
    primary_role = models.ForeignKey(Role)

    def get_fullname(self):
        return '%s %s' % (self.firstname, self.lastname)
    
    def is_section_staff(self):
        return self.primary_role.code in ('section_manager', 'section_assistant')
    
    def is_project_manager(self):
        return self.primary_role.code == 'project_manager'
    
    def is_in_section(self, section):
        return UserSection.objects.filter(user=self.user, section=section).exists()
    
    def is_manage_project(self, project):
        return ProjectManager.objects.filter(user=self.user, project=project).exists()

class UserSection(models.Model):
    user = models.ForeignKey(User)
    section = models.ForeignKey('domain.Section')

class ProjectResponsibility(models.Model): # for section cordinator
    user = models.ForeignKey(User)
    project = models.ForeignKey('domain.Project')

class ProjectManager(models.Model): # for project manager
    user = models.ForeignKey(User)
    project = models.ForeignKey('domain.Project')

