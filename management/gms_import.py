# -*- encoding: utf-8 -*-

HOST = 'http://61.90.139.134/gms/api/'
APIKEY = 'WY0sSJA693sZsHRxT7oTwdzVM83mK0XQcffTYPPes1YUklgH6X5oxQ0xjv8WneG'

PLAN_YEAR = ('55', '54', '53', '52', '51', '50')

SMS_PLAN_VIEW_URL = HOST + '?view=SMS_PLAN_VIEW&format=json&page=0&general=1&apikey=' + APIKEY
SMS_CONTRACT_VIEW_URL = HOST + '?view=SMS_CONTRACT_VIEW&format=json&page=0&general=1&apikey=' + APIKEY
SMS_CONTRACT_MONEY_URL = HOST + '?view=SMS_Contract_Money&format=json&page=0&general=1&apikey=' + APIKEY
SMS_PV_PAYMENT_VIEW_URL = HOST + '?view=SMS_PV_PAYMENT_VIEW&format=json&page=0&general=1&apikey=' + APIKEY

import datetime
import urllib

from django.utils import simplejson

from budget.models import *
from domain.models import *

def convert_to_date(str):
    try:
        (year_str, month_str, date_str) = str.split(' ')[0].split('-')
        return datetime.date(int(year_str), int(month_str), int(date_str))
    except:
        return None

def convert_to_int(str):
    if not str:
        return 0
    else:
        try:
            return int(float(str))
        except:
            return 0

def find_project(raw_project_list, project_code):
    for raw_project in raw_project_list:
        if raw_project['ProjectCode'] == project_code:
            return raw_project
    return None

def import_gms(imported_by):
    raw_project_list = []

    # Retrieve project data

    for section in Section.objects.all():
        import_url = urllib.urlopen(SMS_CONTRACT_VIEW_URL + '&where=sectioncode%3d%27' + section.ref_no + '%27')
        raw_project_list.append('')
        raw_project_list[-1:] = simplejson.loads(import_url.read()) # Append list to list
    
    for raw_project in raw_project_list:
        try:
            section = Section.objects.get(ref_no=raw_project['SectionCode'])
        except Section.DoesNotExist:
            continue

        try:
            project = Project.objects.get(ref_no=raw_project['ProjectCode'])
        except Project.DoesNotExist:
            project = Project.objects.create(
                section=section,
                ref_no=raw_project['ProjectCode'],
                contract_no=raw_project['ContractNo'],
                name=raw_project['ProjectThai'],
                manager_name='%s %s %s' % (raw_project['Resp_Title'], raw_project['Resp_Fname'], raw_project['Resp_Lname']),
                start_date=convert_to_date(raw_project['DateStart']),
                end_date=convert_to_date(raw_project['DateFinish']),
                status=raw_project['ProjectStatusName'],
                created_by=imported_by,
            )
            
        else:
            # Update project
            project.section = section
            project.contract_no = raw_project['ContractNo']
            project.name = raw_project['ProjectThai']
            project.manager_name = '%s %s %s' % (raw_project['Resp_Title'], raw_project['Resp_Fname'], raw_project['Resp_Lname'])
            project.start_date = convert_to_date(raw_project['DateStart'])
            project.end_date = convert_to_date(raw_project['DateFinish'])
            project.status = raw_project['ProjectStatusName']
            project.save()
        
        # assign report for a project that is still active by checking from status text
        if project.is_active():
            for report in Report.objects.filter(section=section):
                ReportAssignment.objects.get_or_crete(report=report, project=project)
    
    # Retrieve budget data

    import_url = urllib.urlopen(SMS_CONTRACT_MONEY_URL)
    raw_money_list = simplejson.loads(import_url.read())

    for raw_money in raw_money_list:
        try:
            project = Project.objects.get(ref_no=raw_money['ProjectCode'])
        except Project.DoesNotExist:
            continue
        
        try:
            budget_schedule = BudgetSchedule.objects.get(project=project, cycle=int(raw_money['Cno']))
        except BudgetSchedule.DoesNotExist:
            budget_schedule = BudgetSchedule.objects.create(
                project=project,
                cycle=int(raw_money['Cno']),
                start_date=convert_to_date(raw_money['DateStart']),
                end_date=convert_to_date(raw_money['DateEnd']),
                due_date=convert_to_date(raw_money['DateDue']),
                grant_budget=convert_to_int(raw_money['MoneyHead']) + convert_to_int(raw_money['MoneyOperate']),
            )

        else:
            budget_schedule.start_date = convert_to_date(raw_money['DateStart'])
            budget_schedule.end_date = convert_to_date(raw_money['DateEnd'])
            budget_schedule.due_date = convert_to_date(raw_money['DateDue'])
            budget_schedule.grant_budget = convert_to_int(raw_money['MoneyHead']) + convert_to_int(raw_money['MoneyOperate'])
            budget_schedule.save()
    
    import_url = urllib.urlopen(SMS_PV_PAYMENT_VIEW_URL)
    raw_payment_list = simplejson.loads(import_url.read())

    for raw_payment in raw_payment_list:
        try:
            project = Project.objects.get(ref_no=raw_payment['ProjectCode'])
        except Project.DoesNotExist:
            continue
        
        try:
            budget_schedule = BudgetSchedule.objects.get(project=project, cycle=int(raw_money['Cno']))
        except BudgetSchedule.DoesNotExist:
            continue

        else:
            budget_schedule.claimed_on = convert_to_date(raw_payment['PayDate'])
            budget_schedule.claim_budget = convert_to_int(raw_payment['Pay'])
            budget_schedule.save()



    




"""
    raw_plan_list = []
    for year in PLAN_YEAR:
        import_url = urllib.urlopen(SMS_PLAN_VIEW_URL + '&where=pbyear%3d%27' + year + '%27')

        # Append to raw_plan_list
        raw_plan_list.append('')
        raw_plan_list[-1:] = simplejson.loads(import_url.read()) # Append list to list
    

    #import_url = urllib.urlopen(SMS_CONTRACT_VIEW_URL)
    #raw_project_list = simplejson.loads(import_url.read())

    #import_url = urllib.urlopen(SMS_PV_PAYMENT_VIEW_URL)
    #raw_money_list = simplejson.loads(import_url.read())

    # Insert projects to SMS

    for section in Section.objects.all():
        import_url = urllib.urlopen(SMS_CONTRACT_VIEW_URL + '&where=sectioncode%3d%27' + section.ref_no + '%27')
        raw_project_list = simplejson.loads(import_url.read())
    

    for raw_plan in raw_plan_list:
        try:
            master_plan = MasterPlan.objects.get(ref_no=int(raw_plan['PBMCode']))
        except:
            continue

        raw_project = find_project(raw_project_list, raw_plan['ProjectCode'])

        if raw_project:
            try:
                project = Project.objects.get(ref_no=raw_plan['ProjectCode'])
            except Project.DoesNotExist:
                project = Project.objects.create(
                    master_plan=master_plan,
                    ref_no=raw_plan['ProjectCode'],
                    contract_no=raw_project['ContractNo'],
                    name=raw_project['ProjectThai'],
                    manager_name='%s %s %s' % (raw_project['Resp_Title'], raw_project['Resp_Fname'], raw_project['Resp_Lname']),
                    start_date=convert_to_date(raw_project['DateStart']),
                    end_date=convert_to_date(raw_project['DateFinish']),
                    created_by=imported_by,
                )
                
            else:
                # Update project
                project.name = raw_project['ProjectThai']
                project.manager_name = '%s %s %s' % (raw_project['Resp_Title'], raw_project['Resp_Fname'], raw_project['Resp_Lname'])
                project.start_date = convert_to_date(raw_project['DateStart'])
                project.end_date = convert_to_date(raw_project['DateFinish'])
                project.save()

        else:
            continue
"""
"""
    for raw_money in raw_money_list:
        try:
            project = Project.objects.get(ref_no=raw_money['ProjectCode'])
        except Project.DoesNotExist:
            logfile.write('ERROR: Project not found in SMS_PV_PAYMENT_VIEW_URL [ProjectCode="%s"]\n' % raw_money['ProjectCode'])
            continue
        
        if raw_money['PayDate']:
            try:
                budget_schedule = BudgetSchedule.objects.get(project=project, schedule_on=convert_to_date(raw_money['PayDate']))
            except BudgetSchedule.DoesNotExist:
                budget_schedule = BudgetSchedule.objects.create(
                    project=project,
                    schedule_on=convert_to_date(raw_money['PayDate']),
                    claimed_on=convert_to_date(raw_money['PayDate']),
                    grant_budget=int(float(raw_money['Pay'])),
                    claim_budget=int(float(raw_money['Pay'])),
                )

                revision = BudgetScheduleRevision.objects.create(
                    schedule=budget_schedule,
                    grant_budget=budget_schedule.grant_budget,
                    claim_budget=budget_schedule.claim_budget,
                    schedule_on=budget_schedule.schedule_on,
                    revised_by=admin_user
                )

                stat_budget_created = stat_budget_created + 1
"""
    