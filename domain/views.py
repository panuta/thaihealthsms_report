# -*- encoding: utf-8 -*-

import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from common.utilities import make_random_user_password

from accounts.models import UserProfile, UserSection, ProjectManager

from forms import *
from models import *

@login_required
def view_organization(request):
    sections = Section.objects.all().order_by('order_number')
    return render(request, 'domain/organization.html', {'sections':sections})

## ADMINISTRATION ##

@login_required
def view_manage_users(request):
    user_profiles = UserProfile.objects.filter(primary_role__in=(Group.objects.get(name='section_manager'), Group.objects.get(name='section_assistant'))).order_by('firstname', 'lastname')
    
    for user_profile in user_profiles:
        user_profile.user_sections = UserSection.objects.filter(user=user_profile.user)
    
    print user_profiles

    return render(request, 'domain/admin/manage_users_section.html', {'active_user_menu':'section', 'user_profiles':user_profiles})

@login_required
def view_manage_users_project(request):
    project_managers = ProjectManager.objects.all().distinct('user')
    return render(request, 'domain/admin/manage_users_project.html', {'active_user_menu':'project', 'project_managers':project_managers})

@login_required
def view_manage_users_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'domain/admin/manage_users_password.html', {'this_user':user})

@login_required
def view_manage_users_add(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            primary_role = form.cleaned_data['primary_role']

            random_password = make_random_user_password()
            user = User.objects.create_user(email, email, random_password)
            user.is_active = False
            user.save()
            
            user_profile = UserProfile.objects.create(
                user=user,
                firstname=firstname,
                lastname=lastname,
                random_password=random_password,
                primary_role=Group.objects.get(name=primary_role)
            )

            return redirect('view_manage_users_add_responsibility', user_id=user.id)
    
    else:
        form = AddUserForm()

    return render(request, 'domain/admin/manage_users_add.html', {'form':form})

@login_required
def view_manage_users_add_responsibility(request, user_id):
    user = get_object_or_404(User, id=user_id)
    primary_role = user.get_profile().primary_role

    if primary_role in (Group.objects.get(name='section_manager'), Group.objects.get(name='section_assistant')):
        return _add_section_user_responsibility(request, user)
    elif primary_role == Group.objects.get(name='project_manager'):
        return _add_project_manager_responsibility(request, user)
    else:
        raise Http404

def _add_section_user_responsibility(request, user):
    if request.method == 'POST':
        form = AddSectionUserResponsibilityForm(request.POST)
        if form.is_valid():
            sections = form.cleaned_data['sections']

            for section in sections:
                UserSection.objects.create(user=user, section=section)

            user.is_active = True
            user.save()

            messages.success(request, u'เพิ่มผู้ใช้เรียบร้อย')
            return redirect('view_manage_users_password', user_id=user.id)
    
    else:
        form = AddSectionUserResponsibilityForm()

    return render(request, 'domain/admin/manage_users_add_section_user.html', {'form':form, 'this_user':user})

def _add_project_manager_responsibility(request, user):
    if request.method == 'POST':
        form = AddProjectManagerResponsibilityForm(request.POST)
        if form.is_valid():
            project_ref_no = form.cleaned_data['project_ref_no']
            project = get_object_or_404(Project, ref_no=project_ref_no)
            
            project_manager, created = ProjectManager.objects.get_or_create(user=user, project=project)

            if created:
                messages.success(request, u'เพิ่มผู้ใช้เรียบร้อย')
            else:
                messages.warning(request, u'ผู้ใช้เป็นผู้จัดการโครงการนี้อยู่แล้ว')

            if 'submit_continue_button' in request.POST:
                return redirect('view_manage_users_add_responsibility', user_id=user.id)
            else:
                return redirect('view_manage_users_password', user_id=user.id)
    
    else:
        form = AddProjectManagerResponsibilityForm()

    return render(request, 'domain/admin/manage_users_add_project_manager.html', {'form':form, 'this_user':user})

@login_required
def view_manage_users_import(request):

    if request.method == 'POST':
        form = ImportUserForm(request.POST)
        if form.is_valid():
            pass
    
    else:
        form = ImportUserForm()
    
    return render(request, 'domain/admin/manage_users_import.html', {'form':form})

@login_required
def view_manage_import(request):

    if request.method == 'POST':
        import gms
        gms.import_gms(request.user)
        return redirect('view_manage_import')

    return render(request, 'domain/admin/manage_import.html', {})

@login_required
def view_manage_import_details(request):
    return render(request, 'domain/admin/manage_import_details.html', {})

## SECTION PAGE ##

@login_required
def view_section(request, section_ref_no):
    section = get_object_or_404(Section, ref_no=section_ref_no)
    
    today = datetime.date.today()
    current_projects = Project.objects.filter(section=section, start_date__lte=today, end_date__gte=today).order_by('ref_no')
    
    return render(request, 'domain/section_overview.html', {'section':section, 'current_projects':current_projects})

@login_required
def view_section_projects(request, section_ref_no):
    year = datetime.date.today().year
    return _section_projects_in_year(request, section_ref_no, year)

@login_required
def view_section_projects_in_year(request, section_ref_no, year):
    year = int(year) - 543
    return _section_projects_in_year(request, section_ref_no, year)

def _section_projects_in_year(request, section_ref_no, year):
    section = get_object_or_404(Section, ref_no=section_ref_no)
    projects = Project.objects.filter(section=section, start_date__year=year).order_by('ref_no')

    this_year = datetime.date.today().year
    years = range(this_year, this_year-10, -1)
    return render(request, 'domain/section_projects.html', {'section': section, 'projects':projects, 'showing_year':year, 'all_years':years})

## PROJECT ##

@login_required
def view_project_activity(request, project_ref_no):
    project = get_object_or_404(Project, ref_no=project_ref_no)

    return render(request, 'domain/project_activity.html', {'project': project, })

@login_required
def edit_project(request, project_ref_no):
    project = get_object_or_404(Project, ref_no=project_ref_no)

    return render(request, 'domain/project_edit.html', {'project': project, })