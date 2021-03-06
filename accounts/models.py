from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string

from common.utilities import make_random_user_password, generate_md5_base64

class Role(models.Model):
    code = models.CharField(max_length=300, db_index=True, unique=True)
    name = models.CharField(max_length=300)

    def __unicode__(self):
        return self.name

class UserProfileManager(models.Manager):

    def create_user(self, email, first_name, last_name, primary_role, password='', is_finished_register=False):
        username = generate_md5_base64(email)

        if not password:
            random_password = make_random_user_password()
            password = random_password
        else:
            random_password = ''

        user = User.objects.create_user(username, '', password)

        return UserProfile.objects.create(
            user=user,
            email=email,
            first_name=first_name,
            last_name=last_name,
            random_password=random_password,
            primary_role=primary_role,
            is_finished_register=is_finished_register
        )

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    email = models.CharField(max_length=254, unique=True)
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    random_password = models.CharField(max_length=30, null=True, blank=True)
    primary_role = models.ForeignKey(Role)
    is_finished_register = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        """ Update username hash in User object """
        self.user.username = generate_md5_base64(self.email)
        self.user.save()

        super(UserProfile, self).save(*args, **kwargs)

    objects = UserProfileManager()

    def get_fullname(self):
        return '%s %s' % (self.first_name, self.last_name)
    
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

class UserSection(models.Model): # for section manager, section assistant
    user = models.ForeignKey(User)
    section = models.ForeignKey('domain.Section')
    is_active = models.BooleanField(default=True)

class ProjectResponsibility(models.Model): # for section assistant
    user = models.ForeignKey(User)
    project = models.ForeignKey('domain.Project')
    is_active = models.BooleanField(default=True)

class ProjectManager(models.Model): # for project manager
    user = models.ForeignKey(User)
    project = models.ForeignKey('domain.Project')
    is_active = models.BooleanField(default=True)
