import datetime

from django.contrib.sites.models import Site

from accounts.models import ProjectManager
from report.models import *

NOTIFY_DAYS_BEFORE = (0, 2, 7)

def report_notification():
    today = datetime.date.today()
    site = Site.objects.get_current()
    email_datatuple = list()

    user_notifies = {}
    for report in Report.objects.all():
        possible_schedules = get_schedules_until(until_date=today)

        for report_assignment in ReportAssignment.objects.filter(report=report, is_active=True):
            project = report_assignment.project

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
                    if (schedule - today).days == notify_days_before and submitted == False:
                        for manager in ProjectManager.objects.filter(project=project):
                            if not manager.user in user_notifies:
                                user_notifies[manager.user] = []
                            user_notifies[manager.user].append({'report':report, 'project':project, 'schedule':schedule, 'days':notify_days_before})

    email_datatuple = []
    for user in user_notifies.keys():
        user_projects = {}

        for notification in user_notifies[user]:
            if not notification['project'] in user_projects:
                user_projects[notification['project']] = []
            
            user_projects[notification['project']].append(notification)

        email_subject = render_to_string('email/notify_report_subject.txt', {'program': program}).strip(' \n\t')
        email_message = render_to_string('email/notify_report_message.txt', {'site': site, 'atdue_submissions': atdue_submissions, 'beforedue_submissions': beforedue_submissions}).strip(' \n\t')

        email_datatuple.append((email_subject, email_message, settings.SYSTEM_NOREPLY_EMAIL, [user.user.email]))
        
        #for project in user_projects.keys():
        #    user_projects[project].sort()

    send_mass_mail(email_datatuple, fail_silently=True)






#def sort_notification(val1, val2):


def _add_notify_item(notify_user_dict, user, report, project, schedule):
    if not user in notify_user_dict: notify_user_dict[user] = []
    notify_user_dict[user].append({'report':report, 'project':project, 'schedule':schedule})
