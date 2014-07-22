from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from wcproc import *
from singervote import *

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'worldcup.views.home', name='home'),
    #url(r'^worldcup/', include('worldcup.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
#    url(r'^admin/', include(admin.site.urls)),

#    (r'^login/',   worldcup_login),
#    (r'^guess/',   worldcup_guess),
#    (r'^history/(.+)/', worldcup_history),
    (r'^anynomous/(.+)/', singervote_set_anynomous),
    (r'^del/(.+)/', singervote_player_del),
    (r'^add/', singervote_player_add),
    (r'^vote/', singervote_display),
    (r'^admin/', singervote_admin_proc),
#    (r'^test/.+)/', worldcup_test),
)
