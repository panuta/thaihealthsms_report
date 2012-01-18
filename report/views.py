# -*- encoding: utf-8 -*-

import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from private_files.views import get_file as private_files_get_file

from common.utilities import convert_dateid_to_date, format_dateid, split_filename

from domain.models import Project

from forms import *
from models import *

@login_required
def view_report(request, project_id, report_id, schedule_date):
    project = get_object_or_404(Project, pk=project_id)
    report = get_object_or_404(Report, pk=report_id)
    schedule_date = convert_dateid_to_date(schedule_date)

    if not report.is_valid_schedule(schedule_date):
        raise Http404

    try:
        submission = ReportSubmission.objects.get(project=project, report=report, schedule_date=schedule_date)
        submission.attachments = ReportSubmissionAttachment.objects.filter(submission=submission).order_by('-uploaded')
    
    except:
        submission = ReportSubmission(project=project, report=report, schedule_date=schedule_date)
        submission.attachments = []
    
    return render(request, 'report/report_overview.html', {'project':project, 'report':report, 'submission':submission})

@login_required
def submit_project_report_text(request, project_id, report_id, schedule_date):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=project_id)
        report = get_object_or_404(Report, pk=report_id)
        schedule_date = convert_dateid_to_date(schedule_date)
        
        form = SubmitReportTextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['report_text']

            try:
                submission = ReportSubmission.objects.get(project=project, report=report, schedule_date=schedule_date)
                submission.report_text = text
                submission.save()
            except:
                submission = ReportSubmission.objects.create(project=project, report=report, schedule_date=schedule_date, report_text=text, created_by=request.user)
            
        else:
            pass
            # show message
            
        return redirect('view_report', project_id=project_id, report_id=report_id, schedule_date=format_dateid(schedule_date))
        
    else:
        raise Http404

@login_required
def submit_project_report_attachment(request, project_id, report_id, schedule_date):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=project_id)
        report = get_object_or_404(Report, pk=report_id)
        schedule_date = convert_dateid_to_date(schedule_date)

        if not report.is_valid_schedule(schedule_date):
            raise Http404
        
        try:
            submission = ReportSubmission.objects.get(project=project, report=report, schedule_date=schedule_date)
        except:
            submission = ReportSubmission(project=project, report=report, schedule_date=schedule_date)

        form = SubmitReportAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            file_attachment = form.cleaned_data['report_attachment']

            try:
                submission = ReportSubmission.objects.get(project=project, report=report, schedule_date=schedule_date)
            except:
                submission = ReportSubmission.objects.create(project=project, report=report, schedule_date=schedule_date, created_by=request.user)
            
            (file_name, file_ext) = split_filename(file_attachment.name)

            attachment = ReportSubmissionAttachment.objects.create(submission=submission, file_name=file_name, file_ext=file_ext, attachment=file_attachment, uploaded_by=request.user)

        else:
            return render(request, 'report/report_overview.html', {'project':project, 'report':report, 'submission':submission, 'attachment_form':form})
            
        return redirect('view_report', project_id=project_id, report_id=report_id, schedule_date=format_dateid(schedule_date))

    else:
        raise Http404

@login_required
def download_report_attachment(request, uid):
    attachment = get_object_or_404(ReportSubmissionAttachment, uid=uid)
    
    return private_files_get_file(request, 'report', 'ReportSubmissionAttachment', 'attachment', str(attachment.id), '%s.%s' % (attachment.file_name, attachment.file_ext))