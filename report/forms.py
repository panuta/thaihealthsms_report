# -*- encoding: utf-8 -*-

from django import forms

from common.forms import StrippedCharField

class SubmitReportTextForm(forms.Form):
    report_text = StrippedCharField(required=False)

class SubmitReportAttachmentForm(forms.Form):
    report_attachment = forms.FileField()