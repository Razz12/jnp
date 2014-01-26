from django.conf.urls import patterns, include, url
from django.conf import settings

from main.views import rawImageView, postImageView, searchView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'images.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^media/(?P<imagename>[^/]+)$', rawImageView),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^postImage/', postImageView),
    url(r'^search/',searchView)
)

if False and settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
