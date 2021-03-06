# -*- encoding: utf-8 -*-

class ImportError(Exception):

    def __init__(self, raw_str, code=None):
        self.raw_str = raw_str
        self.code = code

import csv

from django.contrib.auth.models import User
from django.utils.encoding import smart_unicode

from common.utilities import make_random_user_password, is_email

from accounts.models import Role, UserProfile, UserSection, ProjectResponsibility, ProjectManager
from domain.models import Section, Project

def import_users(csv_file):
    current_user_type = None
    import_result = []

    for row in csv.reader(csv_file, delimiter=','):

        # Check empty
        if len(row) < 1:
            continue
        
        # User type
        if smart_unicode(row[0]) == u'ผู้อำนวยการสำนัก':
            current_user_type = 1 # Section Manager
            continue
        elif smart_unicode(row[0]) == u'ผู้ประสานงาน':
            current_user_type = 2 # Section Assistant
            print 'SWITCH TO SECTION ASSIST'
            continue
        elif smart_unicode(row[0]) == u'ผู้ดูแลโครงการ':
            current_user_type = 3 # Project Manager
            print 'SWITCH TO PM'
            continue

        # Check email
        if not row[0] or not is_email(row[0]):
            continue

        # Check name
        if not row[1].strip():
            import_result.append({'status':'firstname-missing'})
            continue

        if not row[2].strip():
            import_result.append({'status':'lastname-missing'})
            continue

        email = row[0].strip()
        first_name = row[1].strip()
        last_name = row[2].strip()

        # Section Manager ########################################
        if current_user_type == 1:
            if row[3].strip():
                section_str = row[3].strip()
            else:
                import_result.append({'status':'section-invalid', 'email':email})
                continue
            
            try:
                section = Section.objects.get(ref_no=section_str)
            except Section.DoesNotExist:
                try:
                    section = Section.objects.get(ref_no='0%s' % section_str)
                except Section.DoesNotExist:
                    import_result.append({'status':'section-invalid', 'email':email})
                    continue
            
            try:
                user_profile = UserProfile.objects.get(email=email)
            except UserProfile.DoesNotExist:
                user_profile = UserProfile.objects.create_user(email, first_name, last_name, Role.objects.get(code='section_manager'), '', True)
                UserSection.objects.get_or_create(user=user_profile.user, section=section)

                import_result.append({'status':'success', 'user':user_profile.user, 'role':'section_manager'})
            else:
                import_result.append({'status':'duplicated', 'user':user_profile.user, 'role':'section_manager'})

        # Section Assistant ########################################
        elif current_user_type == 2:
            if row[3].strip():
                section_str = row[3].strip()
            else:
                import_result.append({'status':'section-invalid', 'email':email, 'raw':repr(row)})
                continue
            
            try:
                section = Section.objects.get(ref_no=section_str)
            except Section.DoesNotExist:
                try:
                    section = Section.objects.get(ref_no='0%s' % section_str)
                except Section.DoesNotExist:
                    import_result.append({'status':'section-invalid', 'email':email, 'raw':repr(row), 'section_str':section_str})
                    continue
            
            import_result_projects = []
            projects = []
            for i in range(4, len(row)):
                project_ref_no_str = row[i].strip().replace('-', '')
                
                if project_ref_no_str:
                    try:
                        project = Project.objects.get(ref_no=project_ref_no_str)
                    except Project.DoesNotExist:
                        import_result_projects.append({'status':'project-invalid', 'project_ref_no_str':project_ref_no_str})
                    else:
                        projects.append(project)
            
            user_created = False

            try:
                user_profile = UserProfile.objects.get(email=email)
            except UserProfile.DoesNotExist:
                user_profile = UserProfile.objects.create_user(email, first_name, last_name, Role.objects.get(code='section_assistant'), '', True)
                UserSection.objects.create(user=user_profile.user, section=section)
                user_created = True
            
            for project in projects:
                responsibility, created = ProjectResponsibility.objects.get_or_create(user=user_profile.user, project=project)

                if not created:
                    import_result_projects.append({'status':'duplicated', 'project':project})
                else:
                    import_result_projects.append({'status':'success', 'project':project})
            
            import_result.append({'status':'success' if user_created else 'success-duplicated', 'user':user_profile.user, 'role':'section_assistant', 'project_result':import_result_projects})

        # Project Manager ########################################
        elif current_user_type == 3:
            import_result_projects = []
            projects = []
            for i in range(3, len(row)):
                project_ref_no_str = row[i].strip().replace('-', '')
                
                if project_ref_no_str:
                    try:
                        project = Project.objects.get(ref_no=project_ref_no_str)
                    except Project.DoesNotExist:
                        import_result_projects.append({'status':'project-invalid', 'project_ref_no_str':project_ref_no_str})
                    else:
                        projects.append(project)
            
            user_created = False

            try:
                user_profile = UserProfile.objects.get(email=email)
            except UserProfile.DoesNotExist:
                user_profile = UserProfile.objects.create_user(email, first_name, last_name, Role.objects.get(code='project_manager'), '', True)
                user_created = True
            
            for project in projects:
                manager, created = ProjectManager.objects.get_or_create(user=user_profile.user, project=project)

                if not created:
                    import_result_projects.append({'status':'duplicated', 'project':project})
                else:
                    import_result_projects.append({'status':'success', 'project':project})
            
            import_result.append({'status':'success' if user_created else 'success-duplicated', 'user':user_profile.user, 'role':'project_manager', 'project_result':import_result_projects})

    return import_result
