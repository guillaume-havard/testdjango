from django.conf.urls import patterns, include, url
from django.contrib import admin

# Pour les images /!\ pas bien en production
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sitetest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls')),
    url(r'^miniURL/', include('miniURL.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n'))
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
