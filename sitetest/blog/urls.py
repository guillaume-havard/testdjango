from django.conf.urls import patterns, url

urlpatterns = patterns('blog.views',
    url(r'^accueil$', 'home', name="acc_blog"),
    url(r'^error$', 'error'),
    url(r'^arti$', 'arti'),
)
