# -*- encoding: utf-8 -*-
import os
import re

from datetime import date

from django.conf import settings

from constants import THAI_MONTH_NAME, THAI_MONTH_ABBR_NAME

def format_dateid(datetime):
    return '%02d%02d%d' % (datetime.day, datetime.month, datetime.year)

def format_full_datetime(datetime):
    try:
        return u'%d %s %d เวลา %02d:%02d น.' % (datetime.day, THAI_MONTH_NAME[datetime.month], datetime.year + 543, datetime.hour, datetime.minute)
    except:
        return ''

def format_abbr_datetime(datetime):
    try:
        return u'%d %s %d เวลา %02d:%02d น.' % (datetime.day, THAI_MONTH_ABBR_NAME[datetime.month], datetime.year + 543, datetime.hour, datetime.minute)
    except:
        return ''

def format_full_date(datetime):
    try:
        return u'%d %s %d' % (datetime.day, THAI_MONTH_NAME[datetime.month], datetime.year + 543)
    except:
        return ''

def format_abbr_date(datetime):
    try:
        return u'%d %s %d' % (datetime.day, THAI_MONTH_ABBR_NAME[datetime.month], datetime.year + 543)
    except:
        return ''

def week_since(from_date, to_date=date.today()):
    days_elapse = (to_date - from_date).days

    weeks_elapse = 0
    while days_elapse >= 7:
        weeks_elapse = weeks_elapse + 1
        days_elapse = days_elapse - 7
    
    return (weeks_elapse, days_elapse)

def split_filename(filename):
    (name, ext) = os.path.splitext(filename)
    if ext and ext[0] == '.':
        ext = ext[1:]
    
    return (name, ext)

def convert_dateid_to_date(dateid):
    return date(int(dateid[4:8]), int(dateid[2:4]), int(dateid[0:2]))

allow_password_chars = '0123456789'
random_password_length = 6
def make_random_user_password():
    from random import choice
    return ''.join([choice(allow_password_chars) for i in range(random_password_length)])

email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE)  # domain

def is_email(email):
    return email_re.search(email)