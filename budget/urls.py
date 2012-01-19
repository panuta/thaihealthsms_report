from django.conf.urls.defaults import *

urlpatterns = patterns('budget.views',
    url(r'^project/(?P<project_ref_no>\w+)/budget/$', 'view_project_budget', name='view_project_budget'),
    
)