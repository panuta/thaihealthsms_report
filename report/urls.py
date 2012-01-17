from django.conf.urls.defaults import *

urlpatterns = patterns('report.views',
    url(r'^project/(?P<project_id>\d+)/report/(?P<report_id>\d+)/(?P<schedule_date>\w+)/$', 'view_report', name='view_report'),
    

    

)