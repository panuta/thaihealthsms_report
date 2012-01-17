from django.conf.urls.defaults import *

urlpatterns = patterns('domain.views',
    
    url(r'^organization/$', 'view_organization', name='view_organization'),

    url(r'^sector/(?P<sector_ref_no>\d+)/$', 'view_sector', name='view_sector'),
    url(r'^master_plan/(?P<master_plan_ref_no>\d+)/$', 'view_master_plan', name='view_master_plan'),

    url(r'^project/(?P<project_ref_no>\w+)/report/$', 'view_project_report', name='view_project_report'),
    url(r'^project/(?P<project_ref_no>\w+)/budget/$', 'view_project_budget', name='view_project_budget'),
    url(r'^project/(?P<project_ref_no>\w+)/activities/$', 'view_project_activities', name='view_project_activities'),

    url(r'^project/(?P<project_ref_no>\w+)/edit/$', 'edit_project', name='edit_project'),
)