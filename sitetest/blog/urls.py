from django.conf.urls import patterns, url

urlpatterns = patterns('blog.views',
    url(r'^accueil_base$', 'home_base', name="acc_blog"),
    url(r'^accueil$', 'home'),
    url(r'^error$', 'error'),
    url(r'^arti$', 'arti'),
    url(r'^date$', 'date_actuelle'),
    url(r'^addition/(?P<nombre1>\d+)/(?P<nombre2>\d+)/$', 'addition'),
    url(r'^articles$', 'articles'),
    url(r'^article/(?P<id>\d+)-(?P<slug>.+)', 'lire'),
)
