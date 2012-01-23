# -*- encoding: utf-8 -*-
from django import template
register = template.Library()

import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import NodeList

from common import utilities

from accounts.models import UserProfile

# DATE TIME #################################################################

@register.filter(name='dateid')
def dateid(datetime):
    return utilities.format_dateid(datetime)

@register.filter(name='format_datetime')
def format_datetime(datetime):
    return utilities.format_full_datetime(datetime)

@register.filter(name='format_abbr_datetime')
def format_abbr_datetime(datetime):
    return utilities.format_abbr_datetime(datetime)

@register.filter(name='format_date')
def format_date(datetime):
    return utilities.format_full_date(datetime)

@register.filter(name='format_abbr_date')
def format_abbr_date(datetime):
    return utilities.format_abbr_date(datetime)

@register.filter(name='weeksince')
def weeksince(date):
    (weeks, days) = utilities.week_since(date)
    weeks_text = u'%d สัปดาห์' % abs(weeks) if weeks else ''
    days_text = u'%d วัน' % abs(days) if days else ''
    return '%s%s%s' % (weeks_text, ' ' if weeks_text and days_text else '', days_text)

# PERMISSION #################################################################

class ManageNode(template.Node):
    def __init__(self, nodelist_true, nodelist_false, user, project, role):
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
        self.user = template.Variable(user)
        self.project = template.Variable(project)
        self.role = role.strip(' \"\'')
    
    def render(self, context):
        user = self.user.resolve(context)
        project = self.project.resolve(context)
        role = self.role

        if user.get_profile().is_manage_project(project, role):
            output = self.nodelist_true.render(context)
            return output
        else:
            output = self.nodelist_false.render(context)
            return output

@register.tag(name="manage")
def do_manage(parser, token):
    try:
        tag_name, user, project, role = token.split_contents()
    except ValueError:
        try:
            tag_name, user, project = token.split_contents()
            role = ''
        except ValueError:
            raise template.TemplateSyntaxError, "manage tag raise ValueError"
    
    nodelist_true = parser.parse(('else', 'endmanage'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endmanage',))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    
    return ManageNode(nodelist_true, nodelist_false, user, project, role)
    
# REPORT #################################################################

@register.simple_tag
def print_schedule_outstanding(schedule):
    if not schedule.submitted_on:
        today = datetime.date.today()
        if schedule.schedule_date < today:
            return u'<span class="critical_status">เลยกำหนดส่งมาแล้ว <em>%s</em></span>' % weeksince(schedule.schedule_date)

        elif schedule.schedule_date == today:
            return u'<span class="warning_status">กำหนดส่ง<em>วันนี้</em></span>'

        else:
            if (schedule.schedule_date - today).days <= settings.WARNING_AT_DAYS_BEFORE_DUE:
                return u'<span class="warning_status">จะถึงวันกำหนดส่งในอีก <em>%s</em></span>' % weeksince(schedule.schedule_date)

            else:
                return u'<span class="normal_status">จะถึงวันกำหนดส่งในอีก <em>%s</em></span>' % weeksince(schedule.schedule_date)
    
    else:
        return u'<span class="submitted_status">ส่งเมื่อวันที่ <em>%s</em></span>' % utilities.format_full_datetime(schedule.submitted_on)

@register.simple_tag
def print_report_schedule(report):
    if report.schedule_monthly_length > 1:
        return 'กำหนดส่งทุกวันที่ %d ของทุกๆ %d เดือน' % (report.schedule_monthly_date, report.schedule_monthly_length)
    else:
        return 'กำหนดส่งทุกวันที่ %d ของทุกเดือน' % report.schedule_monthly_date
