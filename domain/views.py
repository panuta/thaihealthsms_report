# -*- encoding: utf-8 -*-

import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from common.utilities import make_random_user_password

from accounts.models import UserProfile, UserSection, ProjectManager

from models import *

@login_required
def view_organization(request):
    sections = Section.objects.all().order_by('order_number')
    return render(request, 'domain/organization.html', {'sections':sections})

## SECTION PAGE ##

@login_required
def view_section(request, section_ref_no):
    section = get_object_or_404(Section, ref_no=section_ref_no)
    
    today = datetime.date.today()
    current_projects = Project.objects.filter(section=section, status__in=('อนุมัติ', 'รอปิดโครงการ')).order_by('-ref_no')
    
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
    projects = Project.objects.filter(section=section, ref_no__startswith=str(year+543)[2:4]).order_by('ref_no')

    this_year = datetime.date.today().year
    years = range(this_year, this_year-10, -1)
    return render(request, 'domain/section_projects.html', {'section': section, 'projects':projects, 'showing_year':year, 'all_years':years})

## PROJECT ##

@login_required
def view_project(request, project_ref_no):
    project = get_object_or_404(Project, ref_no=project_ref_no)
    if request.user.get_profile().is_manage_project(project):
        return redirect('view_project_outstanding_reports', project_ref_no=project_ref_no)
    else:    
        return redirect('view_project_reports', project_ref_no=project_ref_no)

@login_required
def view_project_activity(request, project_ref_no):
    project = get_object_or_404(Project, ref_no=project_ref_no)

    return render(request, 'domain/project_activity.html', {'project': project, })

@login_required
def edit_project(request, project_ref_no):
    project = get_object_or_404(Project, ref_no=project_ref_no)

    return render(request, 'domain/project_edit.html', {'project': project, })