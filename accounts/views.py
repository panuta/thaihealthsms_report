# -*- encoding: utf-8 -*-
import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from common.shortcuts import response_json_success, response_json_error

from domain.models import Section
from report.models import ReportAssignment, ReportSubmission

from forms import *
from models import *

def auth_login(request):
    if request.user.is_authenticated():
        return redirect('view_user_dashboard')
    
    from django.contrib.auth.views import login
    return login(request, authentication_form=EmailAuthenticationForm)

@login_required
def view_user_first_time(request):
    if not request.user.get_profile().random_password:
        return redirect('view_user_dashboard')

    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()

            request.user.get_profile().random_password = ''
            request.user.get_profile().save()
            return redirect('view_user_dashboard')
            
    else:
        form = SetPasswordForm(request.user)
    
    return render(request, 'registration/first_time.html', {'form':form})

@login_required
def view_user_dashboard(request):
    if request.user.get_profile().random_password:
        return redirect('%s' % reverse('view_user_first_time'))

    if request.user.is_superuser:
        return redirect('view_managing_organization')
    
    # Section Manager
    if request.user.get_profile().primary_role == Role.objects.get(code='section_manager'):
        user_sections = UserSection.objects.filter(user=request.user)

        if len(user_sections) == 1:
            return redirect('view_section', section_ref_no=user_sections[0].section.ref_no)
        else:
            return render(request, 'dashboard/dashboard_section_manager.html', {'user_sections':user_sections})
    
    # Section Assistant
    if request.user.get_profile().primary_role == Role.objects.get(code='section_assistant'):
        return redirect('view_section_assistant_unsubmitted_dashboard')
    
    # Project Manager
    if request.user.get_profile().primary_role == Role.objects.get(code='project_manager'):
        user_projects = ProjectManager.objects.filter(user=request.user)

        if len(user_projects) == 1:
            return redirect('view_project', project_ref_no=user_projects[0].project.ref_no)
        else:
            return render(request, 'dashboard/dashboard_project_manager.html', {'user_projects':user_projects})
    
    raise Http404

def view_section_assistant_unsubmitted_dashboard(request):
    responsible_projects = ProjectResponsibility.objects.filter(user=request.user).values_list('project', flat=True)

    # overdue + due
    overdue_submissions = []
    due_submissions = []
    today = datetime.date.today()

    for assignment in ReportAssignment.objects.filter(project__in=responsible_projects, project__status__in=('อนุมัติ', 'รอปิดโครงการ')):
        for submission in assignment.get_outstanding_schedules():
            if submission.schedule_date < today:
                overdue_submissions.append(submission)
            elif submission.schedule_date == today:
                due_submissions.append(submission)
    
    overdue_submissions.sort(key=lambda item:item.schedule_date, reverse=True)

    return render(request, 'dashboard/dashboard_section_assistant_unsubmitted.html', {'overdue_submissions':overdue_submissions, 'due_submissions':due_submissions})

@login_required
def view_section_assistant_submitted_dashboard(request):
    responsible_projects = ProjectResponsibility.objects.filter(user=request.user).values_list('project', flat=True)
    submitted_submissions = ReportSubmission.objects.filter(project__in=responsible_projects).exclude(submitted_on=None).order_by('-submitted_on')[:50]

    return render(request, 'dashboard/dashboard_section_assistant_submitted.html', {'submitted_submissions':submitted_submissions})

@login_required
def edit_section_assistant_responsible_projects(request):
    if not request.user.get_profile().primary_role == Role.objects.get(code='section_assistant'):
        raise Http404

    else:
        user_sections = UserSection.objects.filter(user=request.user)

        if request.method == 'POST':
            form = EditProjectResponsibility(request.POST)
        else:
            form = EditProjectResponsibility(user_sections[0].section, initial={
                'active_projects':ProjectResponsibility.objects.filter(user=request.user, project__section=user_sections[0].section).values_list('project', flat=True),
                'other_projects':ProjectResponsibility.objects.filter(user=request.user, project__section=user_sections[0].section).values_list('project', flat=True)
            })
    
    return render(request, 'dashboard/dashboard_section_assistant_projects.html', {'user_sections':user_sections, 'form':form})

def ajax_edit_responsible_project(request):
    if not request.user.get_profile().primary_role == Role.objects.get(code='section_assistant'):
        raise Http404
        
    else:
        if request.method == 'POST':
            action = request.POST.get('action')
            project_id = request.POST.get('project_id')

            try:
                project = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                return response_json_error('project-notfound')

            if action == 'add':
                ProjectResponsibility.objects.get_or_create(user=request.user, project=project)

            elif action == 'remove':
                try:
                    ProjectResponsibility.objects.get(user=request.user, project=project).delete()
                except ProjectResponsibility.DoesNotExist:
                    pass
                    
            else:
                return response_json_error('action-notfound') 
            
            return response_json_success()
        else:
            raise Http404

@login_required
def view_my_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user_profile = request.user.get_profile()
            user_profile.first_name = form.cleaned_data['first_name']
            user_profile.last_name = form.cleaned_data['last_name']
            user_profile.save()

            messages.success(request, u'แก้ไขข้อมูลส่วนตัวเรียบร้อย')
            return redirect('view_my_profile')
    else:
        form = UserProfileForm(initial=request.user.get_profile().__dict__)

    return render(request, 'accounts/my_profile.html', {'form':form})

@login_required
def view_my_account(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, u'เปลี่ยนรหัสผ่านเรียบร้อย')
            return redirect('view_my_account')

    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'accounts/my_account.html', {'form':form})
