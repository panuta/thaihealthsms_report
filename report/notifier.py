import datetime
from dateutil.relativedelta import *

from django.contrib.sites.models import Site
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string

from report.models import *

NOTIFY_DAYS_BEFORE = (0, 2, 7) # 0 means on the due date
NOTIFY_DAYS_OVERDUE = [] # e.g. 3 means 3 days after due date

def report_notification():
    today = datetime.date.today()
    site = Site.objects.get_current()
    email_datatuple = list()

    user_notifies = {}
    for report in Report.objects.all():
        possible_schedules = report.get_schedules_until(until_date=today+relativedelta(days=+max(NOTIFY_DAYS_BEFORE)))

        for report_assignment in ReportAssignment.objects.filter(report=report, is_active=True):
            project = report_assignment.project

            if not project.is_active():
                continue

            for schedule in possible_schedules:
                try:
                    submission = ReportSubmission.objects.get(report=report, project=project, schedule_date=schedule)
                except ReportSubmission.DoesNotExist:
                    submitted = False
                else:
                    if submission.submitted_on:
                        submitted = True
                    else:
                        submitted = False

                for notify_days_before in NOTIFY_DAYS_BEFORE:
                    if (schedule - today).days == notify_days_before and not submitted:
                        for manager in project.managers():
                            if not manager.user in user_notifies:
                                user_notifies[manager.user] = []
                            user_notifies[manager.user].append({'report':report, 'project':project, 'schedule':schedule, 'days':notify_days_before})

                for notify_days_overdue in NOTIFY_DAYS_OVERDUE:
                    if (today - schedule).days == notify_days_overdue and not submitted:
                        for manager in project.managers():
                            if not manager.user in user_notifies:
                                user_notifies[manager.user] = []
                            user_notifies[manager.user].append({'report':report, 'project':project, 'schedule':schedule, 'days':-notify_days_overdue})

    # Grouping report notification by user
    email_datatuple = []
    for user in user_notifies.keys():
        user_projects = {}

        report_before_due_count = 0
        report_overdue_count = 0

        # Grouping report notification by project
        for notification in user_notifies[user]:
            if not notification['project'] in user_projects:
                user_projects[notification['project']] = []
            
            user_projects[notification['project']].append(notification)

            if notification['days'] >= 0:
                report_before_due_count = report_before_due_count + 1

            if notification['days'] < 0:
                report_overdue_count = report_overdue_count + 1

        # Render email per user
        email_render_dict = {'settings':settings, 'report_before_due_count':report_before_due_count, 'report_overdue_count':report_overdue_count}

        project_reports = []
        for project in user_projects.keys():
            user_projects[project].sort(sort_notification)
            project_reports.append({'project':project, 'schedules':user_projects[project]})
        email_render_dict['project_reports'] = project_reports

        email_subject = render_to_string('email/notify_report_subject.txt', email_render_dict).strip(' \n\t')
        email_message = render_to_string('email/notify_report_message.txt', email_render_dict).strip(' \n\t')

        email_datatuple.append((email_subject, email_message, settings.SYSTEM_NOREPLY_EMAIL, [user.get_profile().email]))

    if email_datatuple:
        send_mass_mail(email_datatuple, fail_silently=True)

def sort_notification(val1, val2):
    return val1['days'] - val2['days']

def _add_notify_item(notify_user_dict, user, report, project, schedule):
    if not user in notify_user_dict: notify_user_dict[user] = []
    notify_user_dict[user].append({'report':report, 'project':project, 'schedule':schedule})
