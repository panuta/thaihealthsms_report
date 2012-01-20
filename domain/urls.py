from django.conf.urls.defaults import *

urlpatterns = patterns('domain.views',

    url(r'^organization/$', 'view_organization', name='view_organization'),

    url(r'^section/(?P<section_ref_no>\d+)/$', 'view_section', name='view_section'),
    url(r'^section/(?P<section_ref_no>\d+)/projects/$', 'view_section_projects', name='view_section_projects'),
    url(r'^section/(?P<section_ref_no>\d+)/projects/(?P<year>\d+)/$', 'view_section_projects_in_year', name='view_section_projects_in_year'),

    url(r'^project/(?P<project_ref_no>\w+)/$', 'view_project', name='view_project'),
    url(r'^project/(?P<project_ref_no>\w+)/activity/$', 'view_project_activity', name='view_project_activity'),
    url(r'^project/(?P<project_ref_no>\w+)/edit/$', 'edit_project', name='edit_project'),
)