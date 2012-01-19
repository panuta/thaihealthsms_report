# -*- encoding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from forms import *
from models import *

def auth_login(request):
    from django.contrib.auth.views import login
    return login(request, authentication_form=EmailAuthenticationForm)

@login_required
def view_user_dashboard(request):
    
    # Section Manager
    if request.user.get_profile().primary_role == Group.objects.get(name='section_manager'):
        sections = UserSection.objects.filter(user=request.user)

        if len(sections) == 1:
            return redirect('view_section', section_ref_no=sections[0].ref_no)
        else:
            return render(request, 'dashboard/dashboard_section_manager.html', {})
    
    # Section Assistant
    if request.user.get_profile().primary_role == Group.objects.get(name='section_manager'):
        sections = UserSection.objects.filter(user=request.user)

        if len(sections) == 1:
            return redirect('view_section', section_ref_no=sections[0].ref_no)
        else:
            return render(request, 'dashboard/dashboard_section_assistant.html', {})
    
    # Project Manager
    if request.user.get_profile().primary_role == Group.objects.get(name='project_manager'):
        projects = ProjectManager.objects.filter(user=request.user)

        if len(projects) == 1:
            return redirect('view_project_report', project_ref_no=projects[0].ref_no)
        else:
            return render(request, 'dashboard/dashboard_project_manager.html', {})
    
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