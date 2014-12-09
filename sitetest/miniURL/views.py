from django.shortcuts import render, redirect, get_object_or_404
from miniURL.models import Redirection
from miniURL.forms import RedirectionForm
import random
import string

# Create your views here.
from numpy.core.umath import minimum


def home(request):
    urls = Redirection.objects.all().order_by('-number_access')
    return render(request, 'miniURL/accueil-url.html', {'urls': urls})



def generer(nb_caracteres):
    caracteres = string.ascii_letters + string.digits
    aleatoire = [random.choice(caracteres) for _ in range(nb_caracteres)]

    return ''.join(aleatoire)

def nouvelle_url(request):
    sauvegarde = False

    if request.method == "POST":
        form = RedirectionForm(request.POST)
        if form.is_valid():
            redirection = Redirection()
            redirection.real_url = form.cleaned_data["real_url"]
            redirection.pseudo = form.cleaned_data["pseudo"]
            redirection.small_url = generer(5)
            redirection.save()

            sauvegarde = True
    else:
        form = RedirectionForm()

    return render(request, 'miniURL/nouv-url.html', locals())

def redirection(request, mini_URL):
    url = get_object_or_404(Redirection, small_url=mini_URL)
    url.number_access += 1
    url.save()
    return redirect(url.real_url)
