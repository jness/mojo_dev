
from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',

    # Root Index and Build 
    (r'^$', 'mfweb.views.builds'),
    (r'^builds/$', 'mfweb.views.builds'),
    (r'^buildinfo/(\S+)$', 'mfweb.views.buildinfo'),

    # Task Index page
    (r'^tasks/$', 'mfweb.views.tasks'),
    (r'^taskinfo/(\S+)$', 'mfweb.views.taskinfo'),

    # MF Users
    (r'^users/$', 'mfweb.views.users'),
    (r'^userinfo/(\S+)$', 'mfweb.views.userinfo'),

    # MF Groups
    (r'^groups/$', 'mfweb.views.groups'),
    (r'^groupinfo/(\S+)$', 'mfweb.views.groupinfo'),

    # MF tags
    (r'^tags/$', 'mfweb.views.tags'),
    (r'^taginfo/(\S+)$', 'mfweb.views.taginfo'),
    
    # MF targets
    (r'^targets/$', 'mfweb.views.targets'),
    (r'^targetinfo/(\S+)$', 'mfweb.views.targetinfo'),
    
    # MF package branch
    (r'^packagebranchinfo/(\S+)$', 'mfweb.views.packagebranchinfo'),

    # Projects Packages
    (r'^packages/$', 'mfweb.views.packages'),
    (r'^packageinfo/(\S+)$', 'mfweb.views.packageinfo'),
    
    # Systems
    (r'^systems/$', 'mfweb.views.systems'),
    (r'^systeminfo/(\S+)$', 'mfweb.views.systeminfo'),

    # Searching 
    (r'^search/$', 'mfweb.views.search'),

    # info pages without a search term
    (r'^buildinfo/$', 'mfweb.views.builds'),
    (r'^taskinfo/$', 'mfweb.views.tasks'),
    (r'^userinfo/$', 'mfweb.views.users'),
    (r'^groupinfo/$', 'mfweb.views.groups'),
    (r'^taginfo/$', 'mfweb.views.tags'),
    (r'^packagebranchinfo/$', 'mfweb.views.packages'),
    (r'^targetinfo/$', 'mfweb.views.targets'),
    (r'^systeminfo/$', 'mfweb.views.systems'),
)

urlpatterns += staticfiles_urlpatterns()
