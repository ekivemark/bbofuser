from django.conf.urls import patterns, include, url
from django.contrib import admin
from apps.developer.views import home_index, agree_to_terms

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'developeraccount.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'apps.developer.views.home_index', name='home'),
    url(r'register$', 'apps.developer.views.agree_to_terms', name="agree_to_terms"),
    url(r'^developer/', include('apps.developer.urls', namespace='developer')),
    url(r'^demo/', include('apps.demo.urls', namespace='demo')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
