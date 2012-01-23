from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('accounts.views',
    url(r'^accounts/login/$', 'auth_login', name='auth_login'),

    url(r'^first_time/$', 'view_user_first_time', name='view_user_first_time'),

    url(r'^dashboard/$', 'view_user_dashboard', name='view_user_dashboard'),

    url(r'^dashboard/reports/unsubmitted/$', 'view_section_assistant_unsubmitted_dashboard', name='view_section_assistant_unsubmitted_dashboard'),
    url(r'^dashboard/reports/submitted/$', 'view_section_assistant_submitted_dashboard', name='view_section_assistant_submitted_dashboard'),
    
    url(r'^dashboard/projects/$', 'edit_section_assistant_responsible_projects', name='edit_section_assistant_responsible_projects'),

    url(r'^ajax/edit_responsible_project/$', 'ajax_edit_responsible_project', name='ajax_edit_responsible_project'),
    
    url(r'^my/$', 'view_my_profile', name='view_my_profile'),
    url(r'^my/account/$', 'view_my_account', name='view_my_account'),
    url(r'^my/account/change_password/$', 'change_my_account_password', name='change_my_account_password'),
)