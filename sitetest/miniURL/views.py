from django.shortcuts import render, redirect, get_object_or_404
from miniURL.models import Redirection
from miniURL.forms import RedirectionForm


# Create your views here.
from numpy.core.umath import minimum


def home(request):
    urls = Redirection.objects.all().order_by('-number_access')
    return render(request, 'miniURL/accueil-url.html', {'urls': urls})


def nouvelle_url(request):
    sauvegarde = False

    if request.method == "POST":
        form = RedirectionForm(request.POST)
        if form.is_valid():
            #redirection = Redirection()
            #redirection.real_url = form.cleaned_data["real_url"]
            #redirection.pseudo = form.cleaned_data["pseudo"]
            #redirection.small_url = generer(5) # il est aussi possible de le faire dans le model en surchargeanr save()
            #redirection.save()
            form.save()
            sauvegarde = True
            return redirect(home)
    else:
        form = RedirectionForm()

    return render(request, 'miniURL/nouv-url.html', locals())

def redirection(request, mini_URL):
    url = get_object_or_404(Redirection, small_url=mini_URL)
    url.number_access += 1
    url.save()
    return redirect(url.real_url)

## Test de classes génériques pour la manipulation de données
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy

class URLCreate(CreateView):
    model = Redirection
    template_name = 'miniURL/nouv-url.html'
    form_class = RedirectionForm
    success_url = reverse_lazy(home)
