from django.conf.urls import patterns, include, url
from django.conf import settings

from main.views import fullTextView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'images.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^full_text/$', fullTextView),
    url(r'^admin/', include(admin.site.urls)),
)

if False and settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
