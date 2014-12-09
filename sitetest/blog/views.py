#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from datetime import datetime
from blog.models import Article
from blog.forms import ContactForm, ArticleForm

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