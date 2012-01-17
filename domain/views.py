# -*- encoding: utf-8 -*-

import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from report.models import Report

from forms import *
from models import *

@login_required
def view_organization(request):
    master_plans = MasterPlan.objects.all().order_by('ref_no')
    sectors = Sector.objects.all().order_by('ref_no')
    return render(request, 'domain/organization.html', {'sectors':sectors, 'master_plans':master_plans})

@login_required
def view_sector(request, sector_ref_no):
    sector = get_object_or_404(Sector, ref_no=sector_ref_no)
    sector_master_plans = SectorMasterPlan.objects.filter(sector=sector).order_by('master_plan__ref_no')
    master_plans = [sector_master_plan.master_plan for sector_master_plan in sector_master_plans]
    
    return render(request, 'domain/sector_overview.html', {'sector':sector, 'master_plans':master_plans})

@login_required
def view_master_plan(request, master_plan_ref_no):
    master_plan = get_object_or_404(MasterPlan, ref_no=master_plan_ref_no)

    today = datetime.date.today()

    current_projects = Project.objects.filter(master_plan=master_plan, start_date__lte=today, end_date__gte=today).order_by('ref_no')
    
    return render(request, 'domain/master_plan_overview.html', {'master_plan': master_plan, 'current_projects':current_projects})

@login_required
def view_project_report(request, project_ref_no):
    project = get_object_or_404(Project, ref_no=project_ref_no)

    reports = Report.objects.filter(master_plan=project.master_plan).order_by('name')

    for report in reports:
        report.recent = report.get_submissions(project, 5)

    return render(request, 'domain/project_report.html', {'project': project, 'reports':reports})

@login_required
def view_project_budget(request, project_ref_no):
    project = get_object_or_404(Project, ref_no=project_ref_no)

    return render(request, 'domain/project_budget.html', {'project': project, })

@login_required
def view_project_activity(request, project_ref_no):
    project = get_object_or_404(Project, ref_no=project_ref_no)

    return render(request, 'domain/project_activity.html', {'project': project, })

@login_required
def edit_project(request, project_ref_no):
    project = get_object_or_404(Project, ref_no=project_ref_no)

    return render(request, 'domain/project_edit.html', {'project': project, })