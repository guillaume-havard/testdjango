from django.conf.urls import patterns, url
from django.views.generic import TemplateView, ListView
from blog.views import FAQView, ListeArticles, LireArticle
from blog.models import Article

urlpatterns = patterns('blog.views',
    url(r'^accueil_base$', 'home_base', name="acc_blog"),
    url(r'^accueil$', 'home'),
    url(r'^error$', 'error'),
    url(r'^arti$', 'arti'),
    url(r'^date$', 'date_actuelle'),
    url(r'^addition/(?P<nombre1>\d+)/(?P<nombre2>\d+)/$', 'addition'),
    url(r'^articles$', 'articles'),
    #url(r'^article/(?P<id>\d+)-(?P<slug>.+)', 'lire'),
    url(r'^nouvel-article/$', 'nouvel_article'),
    url(r'^contact/$', 'contact'),
    url(r'^ncontact/$', 'nouveau_contact'),
    url(r'^acontact/$', 'voir_contacts'),

    #(r'^faq$', FAQView.as_view()),   # Nous demandons la vue correspondant à la classe FAQView
    url(r'^faq', TemplateView.as_view(template_name='blog/faq.html')),

    # Pour affichage de liste de modèle
    # par defaut :
    #    context_object_name="object_list"
    #    template_name="<app>/<model>_list.html"
    url(r'^$', ListView.as_view(model=Article,
                    context_object_name="derniers_articles", # nom de la liste des modele dans le tempalte
                    template_name="blog/articles.html")), # chemin du template
    # M^eme chose mais l'on va redéfinir
    # Le "name" permet d'utiliser la fonctione 'reverse de Django dans un template en utilisant  {% url "blog_liste" %}
    url(r'categorie/(?P<id>\d+)', ListeArticles.as_view(), name="blog_categorie"),

    # Detail view pour voir un objet
    url(r'^article/(?P<pk>\d+)$', LireArticle.as_view(), name='blog_lire'),

    url(r'^test$', TemplateView.as_view(template_name='blog/templates-speciaux.html')),
    url(r'^test_random$', 'test_random'),
    url(r'^messages$', 'voir_messages'),

)
