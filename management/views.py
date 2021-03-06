# -*- encoding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from http import Http403

from common.shortcuts import response_json_success, response_json_error
from common.utilities import make_random_user_password

from accounts.models import Role, UserProfile, UserSection, ProjectManager

from forms import *
from domain.models import *

## MANAGE ORGANIZATION ##

@login_required
def view_managing_organization(request):
    if not request.user.is_staff: raise Http403

    sections = Section.objects.all().order_by('order_number')
    return render(request, 'management/manage_org.html', {'sections':sections})

## MANAGE USERS ##

@login_required
def view_managing_users(request):
    return redirect('view_managing_section_users')

@login_required
def view_managing_section_users(request):
    if not request.user.is_staff: raise Http403

    user_profiles = UserProfile.objects.filter(primary_role__code__in=('section_manager', 'section_assistant')).order_by('first_name', 'last_name')
    
    for user_profile in user_profiles:
        user_profile.user_sections = UserSection.objects.filter(user=user_profile.user)
    
    return render(request, 'management/manage_users_section_users.html', {'active_user_menu':'section', 'user_profiles':user_profiles})

@login_required
def view_managing_project_users(request):
    if not request.user.is_staff: raise Http403

    user_profiles = UserProfile.objects.filter(primary_role__code='project_manager').order_by('first_name', 'last_name')

    for user_profile in user_profiles:
        user_profile.projects = ProjectManager.objects.filter(user=user_profile.user)

    return render(request, 'management/manage_users_project_users.html', {'active_user_menu':'project', 'user_profiles':user_profiles})

@login_required
def view_managing_user_password(request, user_id):
    if not request.user.is_staff: raise Http403

    user = get_object_or_404(User, id=user_id)

    if not user.get_profile().random_password:
        raise Http404
    
    if request.method == 'POST':
        user.get_profile().send_password_email()
        messages.success(request, u'ส่งอีเมลรหัสผ่านให้ผู้ใช้เรียบร้อย')
        return redirect('view_managing_user_password', user_id=user_id)

    return render(request, 'management/manage_users_password.html', {'this_user':user})

@login_required
def add_managing_user(request):
    if not request.user.is_staff: raise Http403

    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            primary_role = form.cleaned_data['primary_role']

            user_profile = UserProfile.objects.create_user(email, first_name, last_name, Role.objects.get(code=primary_role))

            user_profile.user.is_active = False
            user_profile.user.save()

            return redirect('add_managing_user_responsibility', user_id=user_profile.user.id)
    
    else:
        form = AddUserForm()

    return render(request, 'management/manage_users_add.html', {'form':form})

@login_required
def add_managing_user_responsibility(request, user_id):
    if not request.user.is_staff: raise Http403

    user = get_object_or_404(User, id=user_id)

    if user.get_profile().is_section_staff():
        return _add_section_user_responsibility(request, user)

    elif user.get_profile().is_project_manager():
        return _add_project_manager_responsibility(request, user)

    else:
        raise Http404

def _add_section_user_responsibility(request, user):
    if request.method == 'POST':
        form = AddSectionUserResponsibilityForm(request.POST)
        if form.is_valid():
            section = form.cleaned_data['section']

            UserSection.objects.create(user=user, section=section)

            user.is_active = True
            user.save()

            user.get_profile().is_finished_register = True
            user.get_profile().save()

            user.get_profile().send_password_email()

            messages.success(request, u'เพิ่มผู้ใช้ และส่งอีเมลรหัสผ่านให้เรียบร้อย')
            return redirect('view_managing_user_password', user_id=user.id)
    
    else:
        form = AddSectionUserResponsibilityForm()

    return render(request, 'management/manage_users_add_section_user.html', {'form':form, 'this_user':user})

def _add_project_manager_responsibility(request, user):
    if request.method == 'POST':
        form = AddProjectManagerResponsibilityForm(request.POST)
        if form.is_valid():
            project_ref_no = form.cleaned_data['project_ref_no']
            project = Project.objects.get(ref_no=project_ref_no)
            
            project_manager, created = ProjectManager.objects.get_or_create(user=user, project=project)

            user.is_active = True
            user.save()

            user.get_profile().is_finished_register = True
            user.get_profile().save()

            user.get_profile().send_password_email()

            if created:
                messages.success(request, u'เพิ่มผู้ใช้ และส่งอีเมลรหัสผ่านให้เรียบร้อย')
            else:
                messages.warning(request, u'ผู้ใช้เป็นผู้จัดการโครงการนี้อยู่แล้ว')

            if 'submit_continue_button' in request.POST:
                return redirect('add_managing_user_responsibility', user_id=user.id)
            else:
                return redirect('view_managing_user_password', user_id=user.id)
    
    else:
        form = AddProjectManagerResponsibilityForm()

    return render(request, 'management/manage_users_add_project_manager.html', {'form':form, 'this_user':user})

@login_required
def edit_managing_user(request, user_id):
    if not request.user.is_staff: raise Http403

    user = get_object_or_404(User, id=user_id)

    if user.get_profile().is_section_staff():
        return _edit_section_user(request, user)

    elif user.get_profile().is_project_manager():
        return _edit_project_user(request, user)

    else:
        raise Http404

def _edit_section_user(request, user):
    if request.method == 'POST':
        form = EditSectionUserForm(user, request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            section = form.cleaned_data['section']

            if not user.get_profile().is_finished_register:
                user.get_profile().is_finished_register = True

                user.is_active = True
                user.save()
            
            user.get_profile().first_name = first_name
            user.get_profile().last_name = last_name
            user.get_profile().save()

            UserSection.objects.filter(user=user).delete()
            UserSection.objects.create(user=user, section=section)

            messages.success(request, u'แก้ไขข้อมูลผู้ใช้เรียบร้อย')
            return redirect('view_managing_section_users')

    else:
        try:
            section = UserSection.objects.filter(user=user)[0].section
        except:
            section = None

        form = EditSectionUserForm(user, initial={'email':user.get_profile().email, 'first_name':user.get_profile().first_name,  'last_name':user.get_profile().last_name, 'section':section})
    
    return render(request, 'management/manage_users_edit_section_user.html', {'this_user':user, 'form':form})

def _edit_project_user(request, user):
    if request.method == 'POST':
        form = EditProjectUserForm(user, request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            if not user.get_profile().is_finished_register:
                user.get_profile().is_finished_register = True

                user.is_active = True
                user.save()

            user.get_profile().firstname = firstname
            user.get_profile().lastname = lastname
            user.get_profile().save()

            messages.success(request, u'แก้ไขข้อมูลผู้ใช้เรียบร้อย')
            return redirect('view_managing_project_users')

    else:
        form = EditProjectUserForm(user, initial={'email':user.get_profile().email, 'first_name':user.get_profile().first_name,  'last_name':user.get_profile().last_name, })
    
    return render(request, 'management/manage_users_edit_project_user.html', {'this_user':user, 'form':form})

@login_required
def edit_managing_user_projects(request, user_id):
    if not request.user.is_staff: raise Http403

    user = get_object_or_404(User, id=user_id)

    managing_projects = ProjectManager.objects.filter(user=user).order_by('-project__ref_no')

    if request.method == 'POST':
        form = AddProjectManagerResponsibilityForm(request.POST)
        if form.is_valid():
            project_ref_no = form.cleaned_data['project_ref_no']
            project = Project.objects.get(ref_no=project_ref_no)

            project_manager, created = ProjectManager.objects.get_or_create(user=user, project=project)

            if not user.get_profile().is_finished_register:
                user.get_profile().is_finished_register = True
                user.get_profile().save()
            
            messages.success(request, u'เพิ่มโครงการที่รับผิดชอบเรียบร้อย')
            return redirect('edit_managing_user_projects', user_id=user.id)

    else:
        form = AddProjectManagerResponsibilityForm()
    
    return render(request, 'management/manage_users_edit_project_user_projects.html', {'this_user':user, 'form':form, 'managing_projects':managing_projects})

@login_required
def ajax_remove_managing_project(request):
    if not request.user.is_staff: raise Http403

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        project_id = request.POST.get('project_id')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return response_json_error('user-notfound')
        
        if not user.get_profile().is_project_manager():
            return response_json_error('user-invalid')

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return response_json_error('project-notfound')
        
        try:
            ProjectManager.objects.get(user=user, project=project).delete()
        except ProjectManager.DoesNotExist:
            pass
        
        return response_json_success()

@login_required
def deactivate_managing_user(request, user_id):
    if not request.user.is_staff: raise Http403
    user = get_object_or_404(User, id=user_id)

    if not user.is_active:
        raise Http404

    if request.method == 'POST':
        if 'submit-delete' in request.POST:
            user.is_active = False
            user.save()

            messages.success(request, u'ปิดบัญชีผู้ใช้เรียบร้อย')
        
        if user.get_profile().is_section_staff():
            return redirect('view_managing_section_users')

        elif user.get_profile().is_project_manager():
            return redirect('view_managing_project_users')
    
    return render(request, 'management/manage_users_deactivate_user.html', {'this_user':user})

@login_required
def import_managing_users(request):
    if not request.user.is_staff: raise Http403

    if request.method == 'POST':
        form = ImportUserForm(request.POST, request.FILES)
        if form.is_valid():
            user_csv = form.cleaned_data['user_csv']

            from management.users_import import import_users
            import_result = import_users(user_csv)
            
            return render(request, 'management/manage_users_import.html', {'import_result':import_result})
    
    else:
        form = ImportUserForm()
    
    return render(request, 'management/manage_users_import.html', {'form':form})

## GMS IMPORT ##

@login_required
def import_from_gms(request):
    if not request.user.is_staff: raise Http403

    if request.method == 'POST':
        import gms_import
        gms_import.import_gms(request.user)
        return redirect('import_from_gms')

    return render(request, 'management/manage_import.html', {})

@login_required
def view_manage_import_details(request):
    if not request.user.is_staff: raise Http403
    
    return render(request, 'management/manage_import_details.html', {})
