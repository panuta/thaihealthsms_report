# -*- encoding: utf-8 -*-

# Signal after syncdb
from datetime import datetime, date, timedelta

from django.conf import settings
from django.contrib.auth.models import User, Permission
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
    Site.objects.all().update(domain=settings.WEBSITE_DOMAIN, name=settings.WEBSITE_NAME)

    # Role ##################
    admin_role, created = Role.objects.get_or_create(code='administrator', name='ผู้ดูแลระบบ')
    section_mgn_role, created = Role.objects.get_or_create(code='section_manager', name='ผู้อำนวยการสำนัก')
    section_assist_role, created = Role.objects.get_or_create(code='section_assistant', name='ผู้ประสานงานสำนัก')
    pm_role, created = Role.objects.get_or_create(code='project_manager', name='ผู้รับผิดชอบโครงการ')
    
    # Administrator ##################
    admins = settings.ADMINS
    
    from django.core.mail import send_mail
    
    for admin in admins:
        try:
            admin_user_profile = UserProfile.objects.get(email=admin[1])
            
        except UserProfile.DoesNotExist:
            #random_password = User.objects.make_random_password()
            random_password = '1q2w3e4r'
            
            admin_user_profile = UserProfile.objects.create_user(
                email=admin[1],
                first_name=admin[0].split(' ')[0],
                last_name=admin[0].split(' ')[1],
                primary_role=admin_role,
                password=random_password,
                is_finished_register=True
            )

            admin_user_profile.user.is_superuser = True
            admin_user_profile.user.is_staff = True
            admin_user_profile.user.save()

            email_render_dict = {'username':admin[1], 'password':random_password, 'settings':settings, 'site_name':settings.WEBSITE_DOMAIN}
            email_subject = render_to_string('email/create_admin_subject.txt', email_render_dict)
            email_message = render_to_string('email/create_admin_message.txt', email_render_dict)
            
            send_mail(email_subject, email_message, settings.SYSTEM_NOREPLY_EMAIL, [admin[1]])
        
        some_admin = admin_user_profile.user
    
    # Section ##################
    section10, created = Section.objects.get_or_create(ref_no='10', order_number=10, name='ศูนย์เรียนรู้สุขภาวะ', prefix='ฝ่าย', long_abbr_name='ศูนย์เรียนรู้', short_abbr_name='WISH Center')
    section01, created = Section.objects.get_or_create(ref_no='01', order_number=20, name='สำนักสนับสนุนการควบคุมปัจจัยเสี่ยงหลัก', prefix='สำนัก', long_abbr_name='สำนัก 1', short_abbr_name='สำนัก 1')
    section02, created = Section.objects.get_or_create(ref_no='02', order_number=30, name='สำนักสนับสนุนการควบคุมปัจจัยเสี่ยงทางสุขภาพ', prefix='สำนัก', long_abbr_name='สำนัก 2', short_abbr_name='สำนัก 2')
    section03, created = Section.objects.get_or_create(ref_no='03', order_number=40, name='สำนักสนับสนุนสุขภาวะชุมชน', prefix='สำนัก', long_abbr_name='สำนัก 3', short_abbr_name='สำนัก 3')
    section04, created = Section.objects.get_or_create(ref_no='04', order_number=50, name='สำนักสนับสนุนสุขภาวะเด็กเยาวชนและครอบครัว', prefix='สำนัก', long_abbr_name='สำนัก 4', short_abbr_name='สำนัก 4')
    section05, created = Section.objects.get_or_create(ref_no='05', order_number=60, name='สำนักรณรงค์สื่อสารสังคมและส่งเสริมการออกกำลังกาย', prefix='สำนัก', long_abbr_name='สำนัก 5', short_abbr_name='สำนัก 5')
    section06, created = Section.objects.get_or_create(ref_no='06', order_number=70, name='สำนักสร้างสรรค์โอกาสและนวัตกรรม', prefix='สำนัก', long_abbr_name='สำนัก 6', short_abbr_name='สำนัก 6')
    section07, created = Section.objects.get_or_create(ref_no='07', order_number=80, name='สำนักสนับสนุนการพัฒนาระบบสุขภาพ', prefix='สำนัก', long_abbr_name='สำนัก 7', short_abbr_name='สำนัก 7')
    section15, created = Section.objects.get_or_create(ref_no='15', order_number=90, name='สำนักสนับสนุนสุขภาวะองค์กร', prefix='สำนัก', long_abbr_name='สำนัก 8', short_abbr_name='สำนัก 8')
    section16, created = Section.objects.get_or_create(ref_no='16', order_number=95, name='สำนักสนับสนุนสุขภาวะประชากรกลุ่มเฉพาะ', prefix='สำนัก', long_abbr_name='สำนัก 9', short_abbr_name='สำนัก 9')
    section08, created = Section.objects.get_or_create(ref_no='08', order_number=100, name='สำนักพัฒนานโยบายและยุทธศาสตร์', prefix='สำนัก', long_abbr_name='สนย.', short_abbr_name='สนย.')
    section09, created = Section.objects.get_or_create(ref_no='09', order_number=110, name='สำนักพัฒนาภาคีสัมพันธ์และวิเทศสัมพันธ์', prefix='สำนัก', long_abbr_name='สภส.', short_abbr_name='สภส.')
    section00, created = Section.objects.get_or_create(ref_no='00', order_number=120, name='ฝ่ายอำนวยการ', prefix='ฝ่าย', long_abbr_name='ฝ่ายอำนวยการ', short_abbr_name='อำนวยการ')
    section13, created = Section.objects.get_or_create(ref_no='13', order_number=130, name='ฝ่ายสื่อสารองค์กร', prefix='ฝ่าย', long_abbr_name='ฝ่ายสื่อสารองค์กร', short_abbr_name='ฝ่าย CC')
    section12, created = Section.objects.get_or_create(ref_no='12', order_number=140, name='ฝ่ายเทคโนโลยีสารสนเทศ', prefix='ฝ่าย', long_abbr_name='ฝ่ายเทคโนโลยีสารสนเทศ', short_abbr_name='ฝ่าย IT')
    section11, created = Section.objects.get_or_create(ref_no='11', order_number=150, name='ฝ่ายบริหารงานบุคคล', prefix='ฝ่าย', long_abbr_name='ฝ่ายบริหารงานบุคคล', short_abbr_name='ฝ่าย HR')
    section14, created = Section.objects.get_or_create(ref_no='14', order_number=160, name='ฝ่ายบัญชีและการเงิน', prefix='ฝ่าย', long_abbr_name='ฝ่ายบัญชีและการเงิน', short_abbr_name='ฝ่ายบัญชี')
    section17, created = Section.objects.get_or_create(ref_no='17', order_number=170, name='ฝ่ายตรวจสอบภายใน', prefix='ฝ่าย', long_abbr_name='ฝ่ายตรวจสอบภายใน', short_abbr_name='ฝ่ายตรวจสอบภายใน สสส.')
    
    """
    END HERE
    """

    now = datetime.datetime.now()

    # Project
    project1, created = Project.objects.get_or_create(section=section07, ref_no='111111', contract_no='111111', name='This is project 1', status='อนุมัติ', created_by=some_admin)
    project2, created = Project.objects.get_or_create(section=section07, ref_no='222222', contract_no='222222', name='This is project 2', status='อนุมัติ', created_by=some_admin)
    project3, created = Project.objects.get_or_create(section=section07, ref_no='333333', contract_no='333333', name='This is project 3', status='อนุมัติ', created_by=some_admin)

    # Project Manager
    try:
        user_profile1 = UserProfile.objects.get(email='panuta+pm1@gmail.com')
    except UserProfile.DoesNotExist:
        user_profile1 = UserProfile.objects.create_user('panuta+pm1@gmail.com', 'PM1', 'Lastname', pm_role, 'panuta', True)
    
    ProjectManager.objects.get_or_create(user=user_profile1.user, project=project1)

    try:
        user_profile2 = UserProfile.objects.get(email='panuta+pm2@gmail.com')
    except UserProfile.DoesNotExist:
        user_profile2 = UserProfile.objects.create_user('panuta+pm2@gmail.com', 'PM2', 'Lastname', pm_role, 'panuta', True)
    
    ProjectManager.objects.get_or_create(user=user_profile2.user, project=project2)
    ProjectManager.objects.get_or_create(user=user_profile2.user, project=project3)

    # Report
    report1, created = Report.objects.get_or_create(section=section07, name='รายงานผลการดำเนินงานรายเดือน 1', schedule_start=date(2012,3,1), schedule_monthly_length=1, schedule_monthly_date=1, created_by=some_admin)
    report2, created = Report.objects.get_or_create(section=section07, name='รายงานผลการดำเนินงานรายเดือน 2', schedule_start=date(2012,3,1), schedule_monthly_length=1, schedule_monthly_date=6, created_by=some_admin)
    report3, created = Report.objects.get_or_create(section=section07, name='รายงานผลการดำเนินงานรายไตรมาส', schedule_start=date(2012,3,1), schedule_monthly_length=3, schedule_monthly_date=10, created_by=some_admin)

    # Assignment
    ReportAssignment.objects.get_or_create(project=project1, report=report1)
    ReportAssignment.objects.get_or_create(project=project1, report=report2)
    ReportAssignment.objects.get_or_create(project=project1, report=report3)

    ReportAssignment.objects.get_or_create(project=project2, report=report1)

    ReportAssignment.objects.get_or_create(project=project3, report=report2)
    ReportAssignment.objects.get_or_create(project=project3, report=report3)

    # Submission
    submission, created = ReportSubmission.objects.get_or_create(report=report1, project=project1, schedule_date=date(2012, 1, 10), created_by=some_admin)
    submission.submitted_on = now
    submission.save()
    

    #Project.objects.get_or_create(master_plan=master_plan12, ref_no='P110011', contract_no='C10003', name='This is a project somewhere someday', abbr_name='this project', manager_name='Panu Tangchalermkul', start_date=date(2011,8,15), end_date=date(2012,10,8), created_by=some_admin)
    #Project.objects.get_or_create(master_plan=master_plan12, ref_no='P110012', contract_no='C10004', name='Some project somewhere in Thailand', abbr_name='some project', manager_name='Panu Tangchalermkul', start_date=date(2011,8,15), end_date=date(2012,10,8), created_by=some_admin)

    #Report.objects.get_or_create(master_plan=master_plan12, name='Activity Report', schedule_start=date(2012,1,1), schedule_monthly_date=15, schedule_monthly_length=1, created_by=some_admin)
    
    
from django.db.models.signals import post_syncdb
post_syncdb.connect(after_syncdb, dispatch_uid="domain.management")

