from django.conf.urls import patterns, url
from miniURL.views import URLCreate, URLUpdate, URLDelete

urlpatterns = patterns('miniURL.views',
    #url(r'^accueil$', 'home', name='url_liste'),
    #url(r'^nouvelle-url/$', 'nouvelle_url', name='url_nouveau'),
    url(r'^redirection/(?P<mini_URL>.+)', 'redirection', name='url_redirection'),

    url(r'^$', 'home', name='url_liste'),
    url(r'^(?P<page>\d+)$', 'home', name='url_liste'),
    url(r'^nouveau$', URLCreate.as_view(), name='url_nouveau'),
    url(r'^edition/(?P<small_url>\w{6})$', URLUpdate.as_view(), name='url_update'),
    url(r'^supprimer/(?P<small_url>\w{6})$', URLDelete.as_view(), name='url_delete'),

)
