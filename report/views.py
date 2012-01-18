# -*- encoding: utf-8 -*-

import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from common.utilities import convert_dateid_to_date

from domain.models import Project

from models import *

def view_report(request, project_id, report_id, schedule_date):
    project = get_object_or_404(Project, pk=project_id)
    report = get_object_or_404(Report, pk=report_id)
    schedule_date = convert_dateid_to_date(schedule_date)

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
        pass
    else:
        raise Http404

@login_required
def submit_project_report_attachment(request, project_id, report_id, schedule_date):
    if request.method == 'POST':
        pass
    else:
        raise Http404

