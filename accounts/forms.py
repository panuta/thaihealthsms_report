# -*- encoding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from common.forms import StrippedCharField

from domain.models import Project

class EmailAuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    email/password logins.
    """
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(EmailAuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_('Please enter a correct username and password. Note that both fields are case-sensitive.'))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_('This account is inactive.'))
        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(
                _('Your Web browser doesn\'t appear to have cookies enabled. '
                  'Cookies are required for logging in.'))

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache

class ProjectMultipleChoiceField(forms.ModelMultipleChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs['queryset'] = Project.objects.all().order_by('ref_no')
        forms.ModelMultipleChoiceField.__init__(self, *args, **kwargs)

    def label_from_instance(self, obj):
        return u'โครงการ (%s) - %s' % (obj.ref_no, obj.name)

class EditProjectResponsibility(forms.Form):
    active_projects = ProjectMultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple())
    other_projects = ProjectMultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple())

    def __init__(self, section, *args, **kwargs):
        self.section = section
        forms.Form.__init__(self, *args, **kwargs)
        
        self.fields['active_projects'].queryset = Project.objects.filter(section=self.section, status__in=('อนุมัติ', 'รอปิดโครงการ')).order_by('ref_no')
        self.fields['other_projects'].queryset = Project.objects.filter(section=self.section).exclude(status__in=('อนุมัติ', 'รอปิดโครงการ')).order_by('ref_no')
