
HOST = 'http://61.90.139.134/gms/api/'
APIKEY = 'WY0sSJA693sZsHRxT7oTwdzVM83mK0XQcffTYPPes1YUklgH6X5oxQ0xjv8WneG'

PLAN_YEAR = ('55', '54', '53', '52', '51', '50')

SMS_PLAN_VIEW_URL = HOST + '?view=SMS_PLAN_VIEW&format=json&page=0&general=1&apikey=' + APIKEY
SMS_CONTRACT_VIEW_URL = HOST + '?view=SMS_CONTRACT_VIEW&format=json&page=0&general=1&apikey=' + APIKEY
#SMS_CONTRACT_MONEY_URL = HOST + '?view=SMS_Contract_Money&format=json&page=0&general=1&apikey=' + APIKEY
SMS_PV_PAYMENT_VIEW_URL = HOST + '?view=SMS_PV_PAYMENT_VIEW&format=json&page=0&general=1&apikey=' + APIKEY

import datetime
import urllib

from django.utils import simplejson

from domain.models import *

def convert_to_date(str):
    (year_str, month_str, date_str) = str.split(' ')[0].split('-')
    return datetime.date(int(year_str), int(month_str), int(date_str))

def find_project(raw_project_list, project_code):
    for raw_project in raw_project_list:
        if raw_project['ProjectCode'] == project_code:
            return raw_project
    return None

def import_gms(imported_by):

    # Retrieve data as JSON format from GMS

    raw_plan_list = []
    for year in PLAN_YEAR:
        import_url = urllib.urlopen(SMS_PLAN_VIEW_URL + '&where=pbyear%3d%27' + year + '%27')

        # Append to raw_plan_list
        raw_plan_list.append('')
        raw_plan_list[-1:] = simplejson.loads(import_url.read()) # Append list to list

    import_url = urllib.urlopen(SMS_CONTRACT_VIEW_URL)
    raw_project_list = simplejson.loads(import_url.read())

    import_url = urllib.urlopen(SMS_PV_PAYMENT_VIEW_URL)
    raw_money_list = simplejson.loads(import_url.read())

    # Insert plans and projects to SMS

    stat_project_created = 0
    stat_budget_created = 0

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
    