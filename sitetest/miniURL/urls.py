from django.conf.urls import patterns, url
from miniURL.views import URLCreate

urlpatterns = patterns('miniURL.views',
    #url(r'^accueil$', 'home', name='url_liste'),
    #url(r'^nouvelle-url/$', 'nouvelle_url', name='url_nouveau'),
    url(r'^redirection/(?P<mini_URL>.+)', 'redirection', name='url_redirection'),

    url(r'^$', 'home', name='url_liste'),
    url(r'^nouveau$', URLCreate.as_view(), name='url_nouveau'),

)
