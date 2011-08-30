from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import redirect_to

urlpatterns = patterns('',

    # Root Index and Build 
    (r'^$', redirect_to, {'url': '/build/'}),
    (r'^search/$', 'mfweb.views.search'),
    (r'^(\S+)/(\S+)?$', 'mfweb.views.mf_request'),
)

urlpatterns += staticfiles_urlpatterns()
