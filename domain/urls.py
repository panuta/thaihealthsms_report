from django.conf.urls.defaults import *

urlpatterns = patterns('domain.views',

    url(r'^organization/$', 'view_organization', name='view_organization'),

    url(r'^manage/users/$', 'view_manage_users', name='view_manage_users'),
    url(r'^manage/users/project/$', 'view_manage_users_project', name='view_manage_users_project'),

    url(r'^manage/users/add/$', 'view_manage_users_add', name='view_manage_users_add'),
    url(r'^manage/users/(?P<user_id>\d+)/add/responsibility/$', 'view_manage_users_add_responsibility', name='view_manage_users_add_responsibility'),
    url(r'^manage/users/(?P<user_id>\d+)/password/$', 'view_manage_users_password', name='view_manage_users_password'),
    
    url(r'^manage/users/import/$', 'view_manage_users_import', name='view_manage_users_import'),

    url(r'^manage/import/$', 'view_manage_import', name='view_manage_import'),
    url(r'^manage/import/details/$', 'view_manage_import_details', name='view_manage_import_details'),

    url(r'^section/(?P<section_ref_no>\d+)/$', 'view_section', name='view_section'),
    url(r'^section/(?P<section_ref_no>\d+)/projects/$', 'view_section_projects', name='view_section_projects'),
    url(r'^section/(?P<section_ref_no>\d+)/projects/(?P<year>\d+)/$', 'view_section_projects_in_year', name='view_section_projects_in_year'),

    url(r'^project/(?P<project_ref_no>\w+)/activity/$', 'view_project_activity', name='view_project_activity'),
    url(r'^project/(?P<project_ref_no>\w+)/edit/$', 'edit_project', name='edit_project'),
)