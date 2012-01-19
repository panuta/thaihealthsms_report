# -*- encoding: utf-8 -*-
from django import template
register = template.Library()

from django.conf import settings
from django.core.urlresolvers import reverse

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

# NAVIGATION #################################################################

@register.simple_tag
def display_header_navigation(user):

    if user.is_superuser:
        html = ''
    else:
        html = u'<a href="%s" class="home">หน้า Dashboard</a> |' % reverse('view_user_dashboard')
    
    if user.is_staff:
        html = html + u'<a href="%s" class="admin">จัดการระบบ</a> |' % reverse('view_manage_users')
    
    html = html + u'<a href="%s" class="org">ผังองค์กร</a> |' % reverse('view_organization')
    
    return html