# -*- encoding: utf-8 -*-

from django import forms

from common.forms import StrippedCharField

from domain.models import Section, Project

class AddUserForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'span6'}))
    firstname = StrippedCharField(max_length=300, widget=forms.TextInput(attrs={'class':'span5'}))
    lastname = StrippedCharField(max_length=300, widget=forms.TextInput(attrs={'class':'span5'}))
    primary_role = forms.ChoiceField(choices=(('section_manager', 'ผู้อำนวยการสำนัก'), ('section_assistant', 'ผู้ประสานงานสำนัก'), ('project_manager', 'ผู้รับผิดชอบโครงการ')))

class AddSectionUserResponsibilityForm(forms.Form):
    section = forms.ModelChoiceField(queryset=Section.objects.all(), widget=forms.RadioSelect(), empty_label=None)

class AddProjectManagerResponsibilityForm(forms.Form):
    project_ref_no = StrippedCharField(max_length=100, widget=forms.TextInput(attrs={'class':'span4'}))

    def clean_project_ref_no(self):
        project_ref_no = self.cleaned_data['project_ref_no']

        try:
            project = Project.objects.get(ref_no=project_ref_no)
        except Project.DoesNotExist:
            raise forms.ValidationError('รหัสโครงการไม่ถูกต้อง')

        return project_ref_no

class ImportUserForm(forms.Form):
    user_csv = forms.FileField()

class EditSectionUserForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'span6'}))
    firstname = StrippedCharField(max_length=300, widget=forms.TextInput(attrs={'class':'span5'}))
    lastname = StrippedCharField(max_length=300, widget=forms.TextInput(attrs={'class':'span5'}))
    section = forms.ModelChoiceField(queryset=Section.objects.all(), widget=forms.RadioSelect(), empty_label=None)

class EditProjectUserForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'span6'}))
    firstname = StrippedCharField(max_length=300, widget=forms.TextInput(attrs={'class':'span5'}))
    lastname = StrippedCharField(max_length=300, widget=forms.TextInput(attrs={'class':'span5'}))