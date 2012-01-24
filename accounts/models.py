from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string

class Role(models.Model):
    code = models.CharField(max_length=300, db_index=True, unique=True)
    name = models.CharField(max_length=300)

    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    firstname = models.CharField(max_length=300)
    lastname = models.CharField(max_length=300)
    random_password = models.CharField(max_length=30, null=True, blank=True)
    primary_role = models.ForeignKey(Role)

    def __unicode__(self):
        return '%s %s' % (self.firstname, self.lastname)

    def get_fullname(self):
        return '%s %s' % (self.firstname, self.lastname)
    
    def is_section_staff(self):
        return self.primary_role.code in ('section_manager', 'section_assistant')
    
    def is_project_manager(self):
        return self.primary_role.code == 'project_manager'
    
    def is_in_section(self, section):
        return UserSection.objects.filter(user=self.user, section=section).exists()
    
    def is_manage_project(self, project, role=None):
        if role == 'pm':
            return ProjectManager.objects.filter(user=self.user, project=project).exists()
        
        elif role == 'assistant':
            return ProjectResponsibility.objects.filter(user=self.user, project=project).exists()

        return ProjectManager.objects.filter(user=self.user, project=project).exists() or ProjectResponsibility.objects.filter(user=self.user, project=project).exists()
    
    def send_password_email(self):
        email_render_dict = {'user_profile':self, 'settings':settings}
        email_subject = render_to_string('email/create_user_subject.txt', email_render_dict)
        email_message = render_to_string('email/create_user_message.txt', email_render_dict)
        
        send_mail(email_subject, email_message, settings.SYSTEM_NOREPLY_EMAIL, [self.user.email])

class UserSection(models.Model):
    user = models.ForeignKey(User)
    section = models.ForeignKey('domain.Section')

class ProjectResponsibility(models.Model): # for section cordinator
    user = models.ForeignKey(User)
    project = models.ForeignKey('domain.Project')

class ProjectManager(models.Model): # for project manager
    user = models.ForeignKey(User)
    project = models.ForeignKey('domain.Project')
