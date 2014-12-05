#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

"""
Toutes les fonctions prendront comme premier argument un objet du type HttpRequest. Toutes les vues doivent forcément retourner une instance de HttpResponse, sans quoi Django générera une erreur.
"""
def home(request):
    """ 
    Exemple de page HTML, non valide pour que l'exemple soit concis 
    Dans le futur ne jamais mettre du code HTML dans une vue.
    Il aura plus sa place dans les templates."""
    text = """<h1>Bienvenue !</h1>
              <p>test test test test test éàêâëä çç!</p>"""
    return HttpResponse(text)
