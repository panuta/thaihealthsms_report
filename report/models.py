import datetime
import uuid

from dateutil.relativedelta import relativedelta
import calendar

from private_files import PrivateFileField

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

def report_media_dir(instance, filename):
    return '%s%s/%s/%s' % (settings.REPORT_ROOT, instance.submission.report.id, instance.submission.project.id, filename)

class Report(models.Model):
    master_plan = models.ForeignKey('domain.MasterPlan')
    name = models.CharField(max_length=500)

    schedule_start = models.DateField()
    schedule_monthly_length = models.IntegerField(default=1)
    schedule_monthly_date = models.IntegerField(default=1) # 0 is end of month

    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)

    def get_schedules_until(self, until_date=datetime.date.today(), and_one_beyond=False):
        result = []

        if self.schedule_monthly_date == 0:
            first_day, schedule_date = calendar.monthrange(self.schedule_start.year, self.schedule_start.month)
            next_schedule = datetime.date(self.schedule_start.year, self.schedule_start.month, schedule_date)
        else:
            if self.schedule_monthly_date < self.schedule_start.day:
                next_schedule = self.schedule_start + relativedelta(months=+self.schedule_monthly_length)
                next_schedule = next_schedule.replace(day=self.schedule_monthly_date)
            else:
                next_schedule = self.schedule_start
                next_schedule = next_schedule.replace(day=self.schedule_monthly_date)
        
        if next_schedule > until_date:
            return result # return empty
        
        result.append(next_schedule)

        while next_schedule <= until_date:
            next_schedule = next_schedule + relativedelta(months=+self.schedule_monthly_length)

            if self.schedule_monthly_date == 0:
                first_day, schedule_date = calendar.monthrange(next_schedule.year, next_schedule.month)
                next_schedule = next_schedule.replace(day=schedule_date)
            
            if not and_one_beyond:
                if next_schedule <= until_date:
                    result.insert(0, next_schedule)
                else:
                    break
            else:
                result.insert(0, next_schedule)
        
        return result
    
    """
    def get_next_schedule(self, from_date=datetime.date.today()):
        if self.schedule_monthly_date == 0:
            first_day, schedule_date = calendar.monthrange(from_date.year, from_date.month)
        else:
            schedule_date = self.schedule_monthly_date

        if from_date.day >= schedule_date:
            schedule_month = from_date.month + 1

            if schedule_month > 12:
                schedule_month = 1
                schedule_year = from_date.year + 1
            else:
                schedule_year = from_date.year
        
        else:
            schedule_month = from_date.month
            schedule_year = from_date.year
        
        return datetime.date(schedule_year, schedule_month, schedule_date)

    def get_previous_schedule(self, from_date=datetime.date.today()):
        if self.schedule_monthly_date == 0:
            first_day, schedule_date = calendar.monthrange(from_date.year, from_date.month)
        else:
            schedule_date = self.schedule_monthly_date

        if from_date.day <= schedule_date:
            schedule_month = from_date.month - 1

            if schedule_month == 0:
                schedule_month = 12
                schedule_year = from_date.year - 1
            else:
                schedule_year = from_date.year

        else:
            schedule_month = from_date.month
            schedule_year = from_date.year
        
        return datetime.date(schedule_year, schedule_month, schedule_date)
    """

    def get_submissions(self, project, depth=0):
        result = []
        created_schedule = set()

        for next_schedule in self.get_schedules_until(and_one_beyond=True):
            try:
                submission = ReportSubmission.objects.get(report=self, project=project, schedule_date=next_schedule)
            except:
                submission = ReportSubmission(report=self, project=project, schedule_date=next_schedule)
        
            result.append(submission)

        for submission in ReportSubmission.objects.filter(report=self, project=project, schedule_date__lt=datetime.date.today()).order_by('-schedule_date'):
            result.append(submission)
        
        if depth > 0:
            return result[:depth]
        else:
            return result
    
    def is_valid_schedule(self, schedule_date):
        if schedule_date < self.schedule_start:
            return False
        else:
            try:
                return self.get_schedules_until(schedule_date)[0] == schedule_date
            except:
                return False

class ReportSubmission(models.Model):
    report = models.OneToOneField(Report)
    project = models.ForeignKey('domain.Project')
    schedule_date = models.DateField()
    report_text = models.TextField(blank=True)
    submitted_on = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='report_submission_created_by')
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, null=True, related_name='report_submission_modified_by')

class ReportSubmissionAttachment(models.Model):
    submission = models.ForeignKey('ReportSubmission')
    uid = models.CharField(max_length=200, db_index=True)
    file_name = models.CharField(max_length=500)
    file_ext = models.CharField(max_length=10)
    attachment = PrivateFileField(upload_to=report_media_dir, max_length=800, null=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User)

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = uuid.uuid4()
        super(ReportSubmissionAttachment, self).save(*args, **kwargs)
