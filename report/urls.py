from django.conf.urls.defaults import *

urlpatterns = patterns('report.views',
    url(r'^project/(?P<project_id>\d+)/report/(?P<report_id>\d+)/(?P<schedule_date>\w+)/$', 'view_report', name='view_report'),
    
    url(r'^project/(?P<project_id>\d+)/report/(?P<report_id>\d+)/(?P<schedule_date>\w+)/submit-text/$', 'submit_project_report_text', name='submit_project_report_text'),
    url(r'^project/(?P<project_id>\d+)/report/(?P<report_id>\d+)/(?P<schedule_date>\w+)/submit-attachment/$', 'submit_project_report_attachment', name='submit_project_report_attachment'),

    

)