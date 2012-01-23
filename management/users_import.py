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
        if len(row) < 1:
            continue
        
        if smart_unicode(row[0]) == u'ผู้อำนวยการสำนัก':
            current_user_type = 1 # Section Manager
            continue
        
        if smart_unicode(row[0]) == u'ผู้ประสานงาน':
            current_user_type = 2 # Section Assistant
            continue
        
        if smart_unicode(row[0]) == u'ผู้ดูแลโครงการ':
            current_user_type = 3 # Project Manager
            continue
    
    
        if row[0] and is_email(row[0]):
            email = row[0]

            if row[1]:
                firstname = row[1]
            else:
                import_result.append({'status':'firstname-missing', 'email':email, 'raw':repr(row)})
            
            if row[1]:
                lastname = row[2]
            else:
                import_result.append({'status':'lastname-missing', 'email':email, 'raw':repr(row)})
            
            # Section Manager ########################################
            if current_user_type == 1:
                if row[3]:
                    section_str = row[3]
                else:
                    import_result.append({'status':'section-missing', 'email':email, 'raw':repr(row)})
                
                try:
                    section = Section.objects.get(ref_no=section_str)
                except Section.DoesNotExist:
                    try:
                        section = Section.objects.get(ref_no='0%s' % section_str)
                    except Section.DoesNotExist:
                        import_result.append({'status':'section-invalid', 'email':email, 'raw':repr(row), 'section_str':section_str})
                
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    user = create_user(email, firstname, lastname, 'section_manager')
                    UserSection.objects.create(user=user, section=section)

                    import_result.append({'status':'success', 'user':user, 'role':'section_manager'})

                else:
                    import_result.append({'status':'duplicated', 'user':user, 'role':'section_manager'})

            # Section Assistant ########################################
            elif current_user_type == 2:
                if row[3]:
                    section_str = row[3]
                else:
                    import_result.append({'status':'section-missing', 'email':email, 'raw':repr(row)})
                
                try:
                    section = Section.objects.get(ref_no=section_str)
                except Section.DoesNotExist:
                    try:
                        section = Section.objects.get(ref_no='0%s' % section_str)
                    except Section.DoesNotExist:
                        import_result.append({'status':'section-invalid', 'email':email, 'raw':repr(row), 'section_str':section_str})
                
                import_result_projects = []
                projects = []
                for i in range(4, len(row)):
                    project_ref_no_str = row[i]
                    
                    if project_ref_no_str:
                        try:
                            project = Project.objects.get(ref_no=project_ref_no_str)
                        except Project.DoesNotExist:
                            import_result_projects.append({'status':'project-invalid', 'project_ref_no_str':project_ref_no_str})
                        else:
                            projects.append(project)
                
                user_created = False
                
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    user = create_user(email, firstname, lastname, 'section_assistant')
                    UserSection.objects.create(user=user, section=section)
                    user_created = True
                
                for project in projects:
                    responsibility, created = ProjectResponsibility.objects.get_or_create(user=user, project=project)

                    if not created:
                        import_result_projects.append({'status':'duplicated', 'project':project})
                    else:
                        import_result_projects.append({'status':'success', 'project':project})
                
                import_result.append({'status':'success' if user_created else 'success-duplicated', 'user':user, 'role':'section_assistant', 'project_result':import_result_projects})

            # Project Manager ########################################
            elif current_user_type == 3:
                import_result_projects = []
                projects = []
                for i in range(3, len(row)):
                    project_ref_no_str = row[i]
                    
                    if project_ref_no_str:
                        try:
                            project = Project.objects.get(ref_no=project_ref_no_str)
                        except Project.DoesNotExist:
                            import_result_projects.append({'status':'project-invalid', 'project_ref_no_str':project_ref_no_str})
                        else:
                            projects.append(project)
                
                user_created = False
                
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    user = create_user(email, firstname, lastname, 'project_manager')
                    user_created = True
                
                for project in projects:
                    manager, created = ProjectManager.objects.get_or_create(user=user, project=project)

                    if not created:
                        import_result_projects.append({'status':'duplicated', 'project':project})
                    else:
                        import_result_projects.append({'status':'success', 'project':project})
                
                import_result.append({'status':'success' if user_created else 'success-duplicated', 'user':user, 'role':'project_manager', 'project_result':import_result_projects})
    
    return import_result

def create_user(email, firstname, lastname, role_code):
    random_password = make_random_user_password()
    user = User.objects.create_user(email, email, random_password)
    
    user_profile = UserProfile.objects.create(
        user=user,
        firstname=firstname,
        lastname=lastname,
        random_password=random_password,
        primary_role=Role.objects.get(code=role_code)
    )

    return user