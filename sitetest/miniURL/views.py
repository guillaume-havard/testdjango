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
    
#############################################################
## Test de classes génériques pour la manipulation de données
# Il existe des noms par défaut pour les templates.
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

class URLCreate(CreateView):
    model = Redirection
    template_name = 'miniURL/nouv-url.html'
    form_class = RedirectionForm
    success_url = reverse_lazy(home)
    
class URLUpdate(UpdateView):
    model = Redirection
    template_name = 'miniURL/nouv-url.html'
    form_class = RedirectionForm
    success_url = reverse_lazy(home)
    
    # Modification des paramètres d'appel
    def get_object(self, queryset=None):
        small_url = self.kwargs.get('small_url', None)
        return get_object_or_404(Redirection, small_url=small_url)
    
    # Modification de ce qui se passe lors de la validation.
    """ Je ne sais pas encore comment les messages fonctionent 
    def form_valid(self, form):
        self.object = form.save()
        # Envoi d'un message à l'utilisateur
        messages.success(self.request, "Votre profil a été mis à jour avec succès.")
        return HttpResponseRedirect(self.get_success_url())
    """

class URLDelete(DeleteView):
    model = Redirection
    context_object_name = "mini_url"
    template_name = 'miniURL/supp-url.html'
    success_url = reverse_lazy(home)

    # Modification des paramètres d'appel
    def get_object(self, queryset=None):
        small_url = self.kwargs.get('small_url', None)
        return get_object_or_404(Redirection, small_url=small_url)      
        
          
