# -*- encoding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User

from common.forms import StrippedCharField
from common.utilities import split_filename

from accounts.models import UserProfile
from domain.models import Section, Project

class AddUserForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'span6'}))
    firstname = StrippedCharField(max_length=300, widget=forms.TextInput(attrs={'class':'span5'}))
    lastname = StrippedCharField(max_length=300, widget=forms.TextInput(attrs={'class':'span5'}))
    primary_role = forms.ChoiceField(choices=(('section_manager', 'ผู้อำนวยการสำนัก'), ('section_assistant', 'ผู้ประสานงานสำนัก'), ('project_manager', 'ผู้รับผิดชอบโครงการ')))

class AddSectionUserResponsibilityForm(forms.Form):
    section = forms.ModelChoiceField(queryset=Section.objects.all(), empty_label=None)

class AddProjectManagerResponsibilityForm(forms.Form):
    project_ref_no = StrippedCharField(max_length=100, widget=forms.TextInput(attrs={'class':'span3'}))

    def clean_project_ref_no(self):
        project_ref_no = self.cleaned_data['project_ref_no']

        try:
            project = Project.objects.get(ref_no=project_ref_no)
        except Project.DoesNotExist:
            raise forms.ValidationError('รหัสโครงการไม่ถูกต้อง')

        return project_ref_no

class ImportUserForm(forms.Form):
    user_csv = forms.FileField()

    def clean_user_csv(self):
        user_csv = self.cleaned_data.get('user_csv')

        if user_csv and split_filename(user_csv.name)[1].lower() != 'csv':
            raise forms.ValidationError('ระบบอ่านได้เฉพาะไฟล์นามสกุล CSV เท่านั้น')
        
        return user_csv

class EditSectionUserForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'span6'}))
    firstname = StrippedCharField(max_length=300, widget=forms.TextInput(attrs={'class':'span5'}))
    lastname = StrippedCharField(max_length=300, widget=forms.TextInput(attrs={'class':'span5'}))
    section = forms.ModelChoiceField(queryset=Section.objects.all(), empty_label='')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        forms.Form.__init__(self, *args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email', '')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        else:
            if user.id != self.user.id:
                raise forms.ValidationError('อีเมลนี้ซ้ำกับผู้ใช้คนอื่นในระบบ')

class EditProjectUserForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'span6'}))
    firstname = StrippedCharField(max_length=300, widget=forms.TextInput(attrs={'class':'span5'}))
    lastname = StrippedCharField(max_length=300, widget=forms.TextInput(attrs={'class':'span5'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        forms.Form.__init__(self, *args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email', '')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        else:
            if user.id != self.user.id:
                raise forms.ValidationError('อีเมลนี้ซ้ำกับผู้ใช้คนอื่นในระบบ')