# -*- encoding: utf-8 -*-

import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from domain.models import Project

from models import *

@login_required
def view_project_budget(request, project_ref_no):
    project = get_object_or_404(Project, ref_no=project_ref_no)
    schedules = BudgetSchedule.objects.filter(project=project).order_by('cycle')
    return render(request, 'domain/project_budget.html', {'project': project, 'budget_schedules':schedules})