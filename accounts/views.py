# -*- encoding: utf-8 -*-

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

from forms import *
from models import *

def auth_login(request):
    from django.contrib.auth.views import login
    response = login(request, authentication_form=EmailAuthenticationForm)

    if request.user.is_authenticated() and request.user.get_profile().random_password:
        return redirect('%s?next=%s' % (reverse('view_user_first_time'), request.POST.get('next')))
    else:
        return response

@login_required
def view_user_first_time(request):
    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()

            request.user.get_profile().random_password = ''
            request.user.get_profile().save()

            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('view_user_dashboard')
            
    else:
        form = SetPasswordForm(request.user)
        next = request.GET.get('next')
    
    return render(request, 'registration/first_time.html', {'form':form, 'next':next})

@login_required
def view_user_dashboard(request):
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
        section = UserSection.objects.filter(user=request.user)[0].section
        responsible_projects = ProjectResponsibility.objects.filter(user=request.user, project__section=section)

        return render(request, 'dashboard/dashboard_section_assistant.html', {'responsible_projects':responsible_projects})
    
    # Project Manager
    if request.user.get_profile().primary_role == Role.objects.get(code='project_manager'):
        user_projects = ProjectManager.objects.filter(user=request.user)

        if len(user_projects) == 1:
            return redirect('view_project', project_ref_no=user_projects[0].project.ref_no)
        else:
            return render(request, 'dashboard/dashboard_project_manager.html', {'user_projects':user_projects})
    
    raise Http404

@login_required
def view_user_dashboard_projects(request):
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
    return render(request, 'accounts/my_account.html', {})

@login_required
def change_my_account_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, u'เปลี่ยนรหัสผ่านเรียบร้อย')
            return redirect('view_my_account')

    else:
        form = PasswordChangeForm(user=request.user)
    
    return render(request, 'accounts/my_account_change_password.html', {'form':form})