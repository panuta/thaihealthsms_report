# -*- encoding: utf-8 -*-

import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from http import Http403

from private_files.views import get_file as private_files_get_file

from common.utilities import convert_dateid_to_date, format_dateid, split_filename

from domain.models import Section, Project

from forms import *
from models import *

@login_required
def view_project_reports(request, project_ref_no): # DONE
    project = get_object_or_404(Project, ref_no=project_ref_no)

    if request.user.get_profile().is_manage_project(project):
        return redirect('view_project_outstanding_reports', project_ref_no=project_ref_no)
    else:
        return redirect('view_project_recent_reports', project_ref_no=project_ref_no)

@login_required
def view_project_outstanding_reports(request, project_ref_no): # DONE
    project = get_object_or_404(Project, ref_no=project_ref_no)

    if request.user.get_profile().is_manage_project(project):
        report_assignments = []

        if project.is_active():
            for report_assignment in ReportAssignment.objects.filter(project=project):
                report_assignment.outstanding_schedules = report_assignment.get_outstanding_schedules()
                
                if report_assignment.outstanding_schedules:
                    report_assignments.append(report_assignment)

        return render(request, 'domain/project_reports_outstanding.html', {'project': project, 'report_assignments':report_assignments})
    
    else:
        raise Http404

@login_required
def view_project_recent_reports(request, project_ref_no): # DONE
    project = get_object_or_404(Project, ref_no=project_ref_no)
    submissions = ReportSubmission.objects.filter(project=project).exclude(submitted_on=None).order_by('-submitted_on')[:20]
    return render(request, 'domain/project_reports_recent.html', {'project': project, 'submissions':submissions})

@login_required
def view_project_all_reports(request, project_ref_no):
    project = get_object_or_404(Project, ref_no=project_ref_no)
    report_assignments = ReportAssignment.objects.filter(project=project).order_by('report__name')
    return render(request, 'domain/project_reports.html', {'project': project, 'report_assignments':report_assignments})

@login_required
def view_project_report(request, project_ref_no, report_id):
    project = get_object_or_404(Project, ref_no=project_ref_no)
    report = get_object_or_404(Report, pk=report_id)

    submissions = []

    if project.is_active():
        schedule_dates = report.get_schedules_until(and_one_beyond=True)
        
        for schedule_date in schedule_dates:
            try:
                submission = ReportSubmission.objects.get(report=report, project=project, schedule_date=schedule_date)
            except:
                submission = ReportSubmission(report=report, project=project, schedule_date=schedule_date)
            
            if not request.user.get_profile().is_manage_project(project):
                if submission.submitted_on:
                    submissions.append(submission)

            else:
                submissions.append(submission)

        for submission in ReportSubmission.objects.filter(project=project, report=report).exclude(submitted_on=None):
            if not submission.schedule_date in schedule_dates:
                submissions.append(submission)

        submissions.sort(key=lambda item:item.schedule_date, reverse=True)
    
    else:
        if request.user.get_profile().is_manage_project(project, role='pm'):
            submissions = ReportSubmission.objects.filter(project=project, report=report).order_by('-schedule_date')
        else:
            submissions = ReportSubmission.objects.filter(project=project, report=report).exclude(submitted_on=None).order_by('-schedule_date')

    return render(request, 'domain/project_report.html', {'project': project, 'report':report, 'submissions':submissions})

@login_required
def view_report(request, project_ref_no, report_id, schedule_date):
    project = get_object_or_404(Project, ref_no=project_ref_no)
    report = get_object_or_404(Report, pk=report_id)
    schedule_date = convert_dateid_to_date(schedule_date)

    if not report.is_valid_schedule(schedule_date):
        print 'invalid schedule'
        raise Http404
    
    try:
        submission = ReportSubmission.objects.get(project=project, report=report, schedule_date=schedule_date)

        if not submission.submitted_on and not request.user.get_profile().is_manage_project(project, role='pm'):
            submission.attachments = []
        else:
            submission.attachments = ReportSubmissionAttachment.objects.filter(submission=submission).order_by('-uploaded')
    
    except:
        submission = ReportSubmission(project=project, report=report, schedule_date=schedule_date)
        submission.attachments = []
    
    if not project.is_active() and not submission.submitted_on and not request.user.get_profile().is_manage_project(project, role='pm'):
        raise Http404

    if not submission.submitted_on and not request.user.get_profile().is_manage_project(project):
        raise Http404
    
    if not submission.submitted_on and not request.user.get_profile().is_manage_project(project, role='pm'):
        submission.report_text = '' # not allow other people to see unfinished report
    
    return render(request, 'report/report_overview.html', {'project':project, 'report':report, 'submission':submission})

@login_required
def submit_project_report(request, project_ref_no, report_id, schedule_date):
    if request.method == 'POST':
        project = get_object_or_404(Project, ref_no=project_ref_no)
        report = get_object_or_404(Report, pk=report_id)
        schedule_date = convert_dateid_to_date(schedule_date)

        if not request.user.get_profile().is_manage_project(project):
            raise Http403
        
        if not report.is_valid_schedule(schedule_date):
            raise Http404

        try:
            submission = ReportSubmission.objects.get(project=project, report=report, schedule_date=schedule_date)
            submission.submitted_on = datetime.datetime.now()
            submission.save()
            messages.success(request, u'ส่งรายงานเรียบร้อย')
        except ReportSubmission.DoesNotExist:
            messages.error(request, u'รายงานยังไม่มีเนื้อหา ไม่สามารถส่งได้')
        
        return redirect('view_report', project_ref_no=project_ref_no, report_id=report_id, schedule_date=format_dateid(schedule_date))
    
    else:
        raise Http404

@login_required
def submit_project_report_text(request, project_ref_no, report_id, schedule_date):
    if request.method == 'POST':
        project = get_object_or_404(Project, ref_no=project_ref_no)
        report = get_object_or_404(Report, pk=report_id)
        schedule_date = convert_dateid_to_date(schedule_date)

        if not request.user.get_profile().is_manage_project(project):
            raise Http403
        
        if not report.is_valid_schedule(schedule_date):
            raise Http404
        
        form = SubmitReportTextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['report_text']

            try:
                submission = ReportSubmission.objects.get(project=project, report=report, schedule_date=schedule_date)
                submission.report_text = text
                submission.save()
            except ReportSubmission.DoesNotExist:
                submission = ReportSubmission.objects.create(project=project, report=report, schedule_date=schedule_date, report_text=text, created_by=request.user)
            
            messages.success(request, u'แก้ไขเนื้อหารายงานเรียบร้อย')
            
        else:
            messages.error(request, u'เนื้อหารายงานไม่อยู่ในรูปแบบที่ถูกต้อง')
            
        return redirect('view_report', project_ref_no=project_ref_no, report_id=report_id, schedule_date=format_dateid(schedule_date))
        
    else:
        raise Http404

@login_required
def submit_project_report_attachment(request, project_ref_no, report_id, schedule_date):
    if request.method == 'POST':
        project = get_object_or_404(Project, ref_no=project_ref_no)
        report = get_object_or_404(Report, pk=report_id)
        schedule_date = convert_dateid_to_date(schedule_date)

        if not request.user.get_profile().is_manage_project(project):
            raise Http403

        if not report.is_valid_schedule(schedule_date):
            raise Http404
        
        try:
            submission = ReportSubmission.objects.get(project=project, report=report, schedule_date=schedule_date)
        except ReportSubmission.DoesNotExist:
            submission = ReportSubmission(project=project, report=report, schedule_date=schedule_date)

        form = SubmitReportAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            file_attachment = form.cleaned_data['report_attachment']

            if not submission.id:
                submission.created_by = request.user
                submission.save()
            
            (file_name, file_ext) = split_filename(file_attachment.name)
            attachment = ReportSubmissionAttachment.objects.create(submission=submission, file_name=file_name, file_ext=file_ext, attachment=file_attachment, uploaded_by=request.user)

            messages.success(request, u'เพิ่มไฟล์แนบเรียบร้อย')

        else:
            return render(request, 'report/report_overview.html', {'project':project, 'report':report, 'submission':submission, 'attachment_form':form})
            
        return redirect('view_report', project_ref_no=project_ref_no, report_id=report_id, schedule_date=format_dateid(schedule_date))

    else:
        raise Http404

@login_required
def download_report_attachment(request, uid):
    attachment = get_object_or_404(ReportSubmissionAttachment, uid=uid)
    return private_files_get_file(request, 'report', 'ReportSubmissionAttachment', 'attachment', str(attachment.id), '%s.%s' % (attachment.file_name, attachment.file_ext))

def delete_report_attachment(request, uid):
    attachment = get_object_or_404(ReportSubmissionAttachment, uid=uid)
    submission = attachment.submission
    report = submission.report
    project = submission.project

    if not request.user.get_profile().is_manage_project(attachment.submission.project):
        raise Http403
    
    if request.method == 'POST':
        if 'submit-delete' in request.POST:
            attachment.attachment.delete()
            attachment.delete()

            messages.success(request, u'ลบไฟล์แนบเรียบร้อย')
        
        return redirect('view_report', project_ref_no=submission.project.ref_no, report_id=report.id, schedule_date=format_dateid(submission.schedule_date))
    
    return render(request, 'report/report_delete_attachment.html', {'attachment':attachment, 'submission':submission, 'report':report, 'project':project})
