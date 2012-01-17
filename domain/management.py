# -*- encoding: utf-8 -*-

# Signal after syncdb
from datetime import datetime, date, timedelta

from django.conf import settings
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from accounts.models import *
from domain.models import *
from report.models import *

import calendar
import random

def after_syncdb(sender, **kwargs):

    some_admin = None

    """
    THIS IS REAL PRODUCTION CODE
    """
    
    # Site Information ###############
    Site.objects.all().update(domain=settings.WEBSITE_ADDRESS, name=settings.WEBSITE_ADDRESS)
    
    # Administrator ##################
    admins = settings.ADMINS
    
    from django.core.mail import send_mail
    
    for admin in admins:
        try:
            admin_user = User.objects.get(username=admin[0])
            some_admin = admin_user.get_profile()
            
        except User.DoesNotExist:
            #random_password = User.objects.make_random_password()
            random_password = '1q2w3e4r'
            admin_user = User.objects.create_user(admin[0], admin[1], random_password)
            admin_user.is_superuser = True
            admin_user.is_staff = True
            admin_user.save()
            
            email_render_dict = {'username':admin[0], 'password':random_password, 'settings':settings, 'site_name':settings.WEBSITE_ADDRESS}
            email_subject = render_to_string('email/create_admin_subject.txt', email_render_dict)
            email_message = render_to_string('email/create_admin_message.txt', email_render_dict)
            
            send_mail(email_subject, email_message, settings.SYSTEM_NOREPLY_EMAIL, [admin[1]])
            
            some_admin, created = UserProfile.objects.get_or_create(user=admin_user, firstname=admin[0], lastname='')
    
    # Sector ##################
    sector1, created = Sector.objects.get_or_create(ref_no=1, name='สำนักสนับสนุนการสร้างสุขภาวะและลดปัจจัยเสี่ยงหลัก')
    sector2, created = Sector.objects.get_or_create(ref_no=2, name='สำนักสนับสนุนการสร้างสุขภาวะและลดปัจจัยเสี่ยงรอง')
    sector3, created = Sector.objects.get_or_create(ref_no=3, name='สำนักสนับสนุนการสร้างสุขภาวะในพื้นที่ชุมชน')
    sector4, created = Sector.objects.get_or_create(ref_no=4, name='สำนักสนับสนุนการเรียนรู้และสุขภาวะองค์กร')
    sector5, created = Sector.objects.get_or_create(ref_no=5, name='สำนักรณรงค์สื่อสารสาธารณะและสังคม')
    sector6, created = Sector.objects.get_or_create(ref_no=6, name='สำนักสนับสนุนโครงการเปิดรับทั่วไป')
    sector7, created = Sector.objects.get_or_create(ref_no=7, name='สำนักสนับสนุนการพัฒนาระบบสุขภาพและบริการสุขภาพ')
    sector8, created = Sector.objects.get_or_create(ref_no=8, name='สำนักพัฒนายุทธศาสตร์ แผนและสมรรถนะ')
    sector9, created = Sector.objects.get_or_create(ref_no=9, name='สำนักพัฒนาวิชาการ')
    
    # Master Plan ##################
    master_plan1, created  = MasterPlan.objects.get_or_create(ref_no=1, name="แผนควบคุมการบริโภคยาสูบ")
    master_plan2, created  = MasterPlan.objects.get_or_create(ref_no=2, name="แผนควบคุมการบริโภคเครื่องดื่มแอลกอฮอล์")
    master_plan3, created  = MasterPlan.objects.get_or_create(ref_no=3, name="แผนสนับสนุนการป้องกันอุบัตเหตุทางถนนและอุบัติภัย")
    master_plan4, created  = MasterPlan.objects.get_or_create(ref_no=4, name="แผนควบคุมปัจจัยเสี่ยงทางสุขภาพ")
    master_plan5, created  = MasterPlan.objects.get_or_create(ref_no=5, name="แผนสุขภาวะประชากรกลุ่มเฉพาะ")
    master_plan6, created  = MasterPlan.objects.get_or_create(ref_no=6, name="แผนสุขภาวะชุมชน")
    master_plan7, created  = MasterPlan.objects.get_or_create(ref_no=7, name="แผนสุขภาวะเด็ก เยาวชน และครอบครัว")
    master_plan8, created  = MasterPlan.objects.get_or_create(ref_no=8, name="แผนสร้างเสริมสุขภาวะในองค์กร")
    master_plan9, created  = MasterPlan.objects.get_or_create(ref_no=9, name="แผนส่งเสริมการออกกำลังกายและกีฬาเพื่อสุขภาพ")
    master_plan10, created  = MasterPlan.objects.get_or_create(ref_no=10, name="แผนสื่อสารการตลาดเพื่อสังคม")
    master_plan11, created  = MasterPlan.objects.get_or_create(ref_no=11, name="แผนสนับสนุนโครงสร้างทั่วไปและนวัตกรรม")
    master_plan12, created  = MasterPlan.objects.get_or_create(ref_no=12, name="แผนสนับสนุนการสร้างเสริมสุขภาพผ่านระบบบริการสุขภาพ")
    master_plan13, created  = MasterPlan.objects.get_or_create(ref_no=13, name="แผนพัฒนาระบบและกลไกสนับสนุนเพื่อการสร้างเสริมสุขภาพ")
    
    SectorMasterPlan.objects.get_or_create(sector=sector1, master_plan=master_plan1)
    SectorMasterPlan.objects.get_or_create(sector=sector1, master_plan=master_plan2)
    SectorMasterPlan.objects.get_or_create(sector=sector1, master_plan=master_plan3)
    SectorMasterPlan.objects.get_or_create(sector=sector2, master_plan=master_plan4)
    SectorMasterPlan.objects.get_or_create(sector=sector2, master_plan=master_plan5)
    SectorMasterPlan.objects.get_or_create(sector=sector3, master_plan=master_plan6)
    SectorMasterPlan.objects.get_or_create(sector=sector4, master_plan=master_plan7)
    SectorMasterPlan.objects.get_or_create(sector=sector4, master_plan=master_plan8)
    SectorMasterPlan.objects.get_or_create(sector=sector5, master_plan=master_plan9)
    SectorMasterPlan.objects.get_or_create(sector=sector5, master_plan=master_plan10)
    SectorMasterPlan.objects.get_or_create(sector=sector6, master_plan=master_plan11)
    SectorMasterPlan.objects.get_or_create(sector=sector7, master_plan=master_plan12)
    SectorMasterPlan.objects.get_or_create(sector=sector7, master_plan=master_plan13)
    SectorMasterPlan.objects.get_or_create(sector=sector8, master_plan=master_plan13)
    SectorMasterPlan.objects.get_or_create(sector=sector9, master_plan=master_plan13)
    
    """
    END HERE
    """

    Project.objects.get_or_create(master_plan=master_plan12, ref_no='P110011', contract_no='C10003', name='This is a project somewhere someday', abbr_name='this project', manager_name='Panu Tangchalermkul', start_date=date(2011,8,15), end_date=date(2012,10,8), created_by=some_admin)
    Project.objects.get_or_create(master_plan=master_plan12, ref_no='P110012', contract_no='C10004', name='Some project somewhere in Thailand', abbr_name='some project', manager_name='Panu Tangchalermkul', start_date=date(2011,8,15), end_date=date(2012,10,8), created_by=some_admin)

    Report.objects.get_or_create(master_plan=master_plan12, name='Activity Report', schedule_start=date(2012,1,1), schedule_monthly_date=15, schedule_monthly_length=1, created_by=some_admin)
    
    
from django.db.models.signals import post_syncdb
post_syncdb.connect(after_syncdb, dispatch_uid="domain.management")

