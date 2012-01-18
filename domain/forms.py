# -*- encoding: utf-8 -*-

from django import forms

from common.forms import StrippedCharField

class AddUserForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'span6'}))
    firstname = StrippedCharField(max_length=300, widget=forms.TextInput(attrs={'class':'span5'}))
    lastname = StrippedCharField(max_length=300, widget=forms.TextInput(attrs={'class':'span5'}))

class ImportUserForm(forms.Form):
    user_csv = forms.FileField()