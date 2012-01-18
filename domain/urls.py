from django.conf.urls.defaults import *

urlpatterns = patterns('domain.views',

    url(r'^organization/$', 'view_organization', name='view_organization'),

    url(r'^manage/users/$', 'view_manage_users', name='view_manage_users'),
    url(r'^manage/users/project/$', 'view_manage_users_project', name='view_manage_users_project'),


    url(r'^manage/users/add/$', 'view_manage_users_add', name='view_manage_users_add'),
    url(r'^manage/users/import/$', 'view_manage_users_import', name='view_manage_users_import'),


    url(r'^manage/import/$', 'view_manage_import', name='view_manage_import'),
    url(r'^manage/import/details/$', 'view_manage_import_details', name='view_manage_import_details'),

    url(r'^sector/(?P<sector_ref_no>\d+)/$', 'view_sector', name='view_sector'),
    url(r'^master_plan/(?P<master_plan_ref_no>\d+)/$', 'view_master_plan', name='view_master_plan'),

    url(r'^project/(?P<project_ref_no>\w+)/report/$', 'view_project_report', name='view_project_report'),
    url(r'^project/(?P<project_ref_no>\w+)/budget/$', 'view_project_budget', name='view_project_budget'),
    url(r'^project/(?P<project_ref_no>\w+)/activity/$', 'view_project_activity', name='view_project_activity'),

    url(r'^project/(?P<project_ref_no>\w+)/edit/$', 'edit_project', name='edit_project'),
)