# -*- encoding: utf-8 -*-

from django import forms

from common.forms import StrippedCharField

from domain.models import Section

class AddUserForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'span6'}))
    firstname = StrippedCharField(max_length=300, widget=forms.TextInput(attrs={'class':'span5'}))
    lastname = StrippedCharField(max_length=300, widget=forms.TextInput(attrs={'class':'span5'}))
    primary_role = forms.ChoiceField(choices=(('section_manager', 'ผู้อำนวยการสำนัก'), ('section_assistant', 'ผู้ประสานงานสำนัก'), ('project_manager', 'ผู้จัดการแผนงาน')))

class AddSectionUserResponsibilityForm(forms.Form):
    sections = forms.ModelMultipleChoiceField(queryset=Section.objects.all(), widget=forms.CheckboxSelectMultiple())

class AddProjectManagerResponsibilityForm(forms.Form):
    project_ref_no = StrippedCharField(max_length=100, widget=forms.TextInput(attrs={'class':'span5'}))

class ImportUserForm(forms.Form):
    user_csv = forms.FileField()