from django.conf.urls import patterns, url

urlpatterns = patterns('miniURL.views',
    url(r'^accueil$', 'home'),
    url(r'^nouvelle-url/$', 'nouvelle_url'),
    url(r'^redirection/(?P<mini_URL>.+)', 'redirection'),

)
