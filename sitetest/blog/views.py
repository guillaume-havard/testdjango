#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.generic import TemplateView, ListView, DetailView
from datetime import datetime
from blog.models import Article, Categorie, Contact
from blog.forms import ContactForm, ArticleForm, NouveauContactForm
from django.contrib import messages

# Create your views here.

"""
Toutes les fonctions prendront comme premier argument un objet du type HttpRequest.
#Toutes les vues doivent forcément retourner une instance de HttpResponse, sans quoi Django générera une erreur.
"""
def home_base(request):
    """ 
    Exemple de page HTML, non valide pour que l'exemple soit concis 
    Dans le futur ne jamais mettre du code HTML dans une vue.
    Il aura plus sa place dans les templates."""
    text = """<h1>Bienvenue !</h1>
              <p>test test test test test éàêâëä çç!</p>"""
    return HttpResponse(text)

def home(request):
    return render(request, 'blog/accueil.html')

def error(request):
    """
    Page d'erreur
    :param request:
    :return:
    """
    raise Http404
    return HttpResponse('pas error')

def arti(request):
    """Rediretion"""
    #return redirect("https://www.djangoproject.com")
    #return redirect('blog.views.home')
    return redirect('acc_blog')

def date_actuelle(request):
    return render(request, 'blog/date.html', {'date': datetime.now()})

def addition(request, nombre1, nombre2):
    total = int(nombre1) + int(nombre2)

    # Retourne nombre1, nombre2 et la somme des deux au tpl
    return render(request, 'blog/addition.html', locals())

def articles(request):
    """ Afficher tous les articles de notre blog """
    articles = Article.objects.all() # Nous sélectionnons tous nos articles
    return render(request, 'blog/articles.html', {'derniers_articles': articles})

def lire(request, id, slug):
    """ Afficher un article complet """
    article = get_object_or_404(Article, id=id, slug=slug)
    return render(request, 'blog/lire.html', {'article':article})


def contact(request):
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        form = ContactForm(request.POST)  # Nous reprenons les données

        if form.is_valid(): # Nous vérifions que les données envoyées sont valides

            # Ici nous pouvons traiter les données du formulaire
            sujet = form.cleaned_data['sujet']
            message = form.cleaned_data['message']
            envoyeur = form.cleaned_data['envoyeur']
            renvoi = form.cleaned_data['renvoi']

            # Nous pourrions ici envoyer l'e-mail grâce aux données que nous venons de récupérer
            # Il faut traiter les infos.
            # Voir nouveau_contact
            envoi = True

    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        form = ContactForm()  # Nous créons un formulaire vide

    return render(request, 'blog/contact.html', locals())

def nouvel_article(request):
    """AJout d'un article via formulaire"""
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            envoi = True
    else:
        form = ArticleForm()

    return render(request, "blog/nouvel-article.html", locals())
    

# Lors de la création de la forme request.FILES est ajouté.    
def nouveau_contact(request):
    sauvegarde = False

    if request.method == "POST":
        form = NouveauContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact = Contact()
            contact.nom = form.cleaned_data["nom"]
            contact.adresse = form.cleaned_data["adresse"]
            contact.photo = form.cleaned_data["photo"]
            contact.save()

            sauvegarde = True
    else:
        form = NouveauContactForm()

    return render(request, 'blog/ncontact.html', locals())    
    
def voir_contacts(request):
    contacts = Contact.objects.all()
    return render(request, 'blog/voir_contacts.html', {'contacts': contacts})

## Voir blog.url
# Pour un affichage sans aucun traitement
class FAQView(TemplateView):
   template_name = "blog/faq.html"  # chemin vers le template à afficher

class ListeArticles(ListView):
    model = Article
    context_object_name = "derniers_articles"
    template_name = "blog/articles.html"
    paginate_by = 5
    #queryset = Article.objects.filter(categorie__id=1) # requettes identiques aux view pour affichage
    # Si argument donné dans l'url
    def get_queryset(self):
       return Article.objects.filter(categorie__id=self.kwargs['id']) # ou si arg non nomé : self.args[0]

    # Pour ajouter des elements au contexte (template)
    def get_context_data(self, **kwargs):
        # Nous récupérons le contexte depuis la super-classe
        context = super(ListeArticles, self).get_context_data(**kwargs)
        # Nous ajoutons la liste des catégories, sans filtre particulier
        context['categories'] = Categorie.objects.all()
        return context
    
class LireArticle(DetailView):
    context_object_name = "article"
    model = Article
    template_name = "blog/lire.html"

    # Pour pouvoir faire des actions sur les modèles avant de les afficher.
    def get_object(self):
        # Nous récupérons l'objet, via la super-classe
        article = super(LireArticle, self).get_object()

        article.nb_vues += 1  # Imaginons un attribut « Nombre de vues »
        article.save()

        return article  # Et nous retournons l'objet à afficher

def test_random(request):
    return render(request, 'blog/test_random.html', {'begin': 1, 'end': 42})

## Messages

# Dans une vue :
# messages.add_message(request, messages.INFO, 'Bonjour visiteur !')

# Il existe plusieurs types de messages pouvant être appelé par les raccourcis suivant :
#messages.debug(request, '%s requêtes SQL ont été exécutées.' % compteur)
#messages.info(request, 'Rebonjour !')
#messages.success(request, 'Votre article a bien été mis à jour.')
#messages.warning(request, 'Votre compte expire dans 3 jours.')
#messages.error(request, 'Cette image n\'existe plus.')

# Exemples messages:

def voir_messages(request):
    articles = Article.objects.all()

    messages.set_level(request, messages.DEBUG) # je suis obligé de le faire sinon je n'ai pas les debug...
    messages.add_message(request, messages.INFO, 'Bonjour visiteur !')
    messages.debug(request, '%s requêtes SQL ont été exécutées.' % articles)
    messages.info(request, 'Rebonjour !')
    messages.success(request, 'Votre article a bien été mis à jour.')
    messages.warning(request, 'Votre compte expire dans 3 jours.')
    messages.error(request, 'Cette image n\'existe plus.')

    return render(request, 'blog/messages.html')

# Il est possible d'ajouter des niveaux de messages
# Les méssages existant n'étatnt que des entier
# messages.add_message(request, 33, 'Bonjour visiteur !')

# Il est aussi possible d'ajouter des tags aux messages
#messages.add_message(request, CRITICAL, 'Une erreur critique est survenue.', extra_tags="fail")

#Le niveau pour lesquel les messages s'affichent est réglable via  la variable MESSAGE_LEVEL de settings.py
# ou via une requette "messages.set_level(request, messages.DEBUG)" en vue


#en utilisant
#messages.info(request, 'Message à but informatif.', fail_silently=True)
# Rien ne se passe si une personne n'a pas activé lesmessage dans son application

### La pagination
# from django.core.paginator import Paginator
# p = Paginator(set, 5) # set classe avec une méthode __len__ ou count
# p.count # nombre d'objet au total
# p.num_pages # 
# p.page_range # liste des pages disponibles
#
# p.page(x) # access à la page x
# p.page(x).object_list

# Utilisation dans miniURL/views.py
