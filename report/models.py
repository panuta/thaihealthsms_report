import datetime

from dateutil.relativedelta import relativedelta
import calendar

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
    created_by = models.ForeignKey('accounts.UserProfile')

    def get_next_schedule(self, from_date=datetime.date.today()):
        if self.schedule_monthly_date == 0:
            first_day, schedule_date = calendar.monthrange(from_date.year, from_date.month)
        else:
            schedule_date = self.schedule_monthly_date

        if from_date.day > schedule_date:
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
    
    def get_submissions(self, project, limit=0):
        result = []
        created_schedule = set()

        next_schedule = self.get_next_schedule()
        try:
            submission = ReportSubmission.objects.get(report=self, project=project, schedule_date=next_schedule)
        except:
            submission = ReportSubmission(report=self, project=project, schedule_date=next_schedule)
        
        result.append(submission)

        next_schedule = self.get_previous_schedule()
        while self.schedule_start <= next_schedule:
            try:
                submission = ReportSubmission.objects.get(report=self, project=project, schedule_date=next_schedule)
            except:
                submission = ReportSubmission(report=self, project=project, schedule_date=next_schedule)
            
            result.append(submission)

            created_schedule.add(next_schedule)
            next_schedule = self.get_previous_schedule(next_schedule)

            if limit > 0 and len(result) == limit:
                break;
        
        submissions = ReportSubmission.objects.filter(report=self, project=project).order_by('-schedule_date')

        for submission in submissions:
            if submission.schedule_date not in created_schedule:
                result.append(submission)
        
        return result

class ReportSubmission(models.Model):
    report = models.OneToOneField(Report)
    project = models.ForeignKey('domain.Project')
    schedule_date = models.DateField()
    report_text = models.TextField(blank=True)
    submitted_on = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('accounts.UserProfile', related_name='report_submission_created_by')
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('accounts.UserProfile', null=True, related_name='report_submission_modified_by')

class ReportSubmissionAttachment(models.Model):
    submission = models.ForeignKey('ReportSubmission')
    uid = models.CharField(max_length=200, db_index=True)
    file_name = models.CharField(max_length=500)
    file_ext = models.CharField(max_length=10)
    attachment = models.FileField(upload_to=report_media_dir, max_length=800, null=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey('accounts.UserProfile')

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = uuid.uuid4()
        super(Publication, self).save(*args, **kwargs)
