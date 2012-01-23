from django.conf.urls.defaults import *

urlpatterns = patterns('report.views',
    url(r'^project/(?P<project_ref_no>\w+)/reports/$', 'view_project_reports', name='view_project_reports'),
    url(r'^project/(?P<project_ref_no>\w+)/reports/all/$', 'view_project_all_reports', name='view_project_all_reports'),
    url(r'^project/(?P<project_ref_no>\w+)/report/(?P<report_id>\d+)/$', 'view_project_report', name='view_project_report'),
    url(r'^project/(?P<project_ref_no>\w+)/reports/recent/$', 'view_project_recent_reports', name='view_project_recent_reports'),
    url(r'^project/(?P<project_ref_no>\w+)/reports/outstanding/$', 'view_project_outstanding_reports', name='view_project_outstanding_reports'),

    url(r'^project/(?P<project_ref_no>\d+)/report/(?P<report_id>\d+)/(?P<schedule_date>\w+)/$', 'view_report', name='view_report'),
    url(r'^project/(?P<project_ref_no>\d+)/report/(?P<report_id>\d+)/(?P<schedule_date>\w+)/submit/$', 'submit_project_report', name='submit_project_report'),
    url(r'^project/(?P<project_ref_no>\d+)/report/(?P<report_id>\d+)/(?P<schedule_date>\w+)/submit-text/$', 'submit_project_report_text', name='submit_project_report_text'),
    url(r'^project/(?P<project_ref_no>\d+)/report/(?P<report_id>\d+)/(?P<schedule_date>\w+)/submit-attachment/$', 'submit_project_report_attachment', name='submit_project_report_attachment'),

    url(r'^report/attachment/download/(?P<uid>[a-zA-Z0-9\-]+)/$', 'download_report_attachment', name='download_report_attachment'),
    url(r'^report/attachment/delete/(?P<uid>[a-zA-Z0-9\-]+)/$', 'delete_report_attachment', name='delete_report_attachment'),

)