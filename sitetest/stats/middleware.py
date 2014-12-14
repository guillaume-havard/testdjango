from django.db.models import F
from stats.models import Page

class StatsMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        """ Incrémente le nombre de page vues à chaque appel de vues """
        try:
            # Le compteur lié à la page est récupéré et incrémenté
            p = Page.objects.get(url=request.path)
            p.nb_visites = F('nb_visites') + 1
            p.save()
        except Page.DoesNotExist:
            # Un nouveau compteur à 1 par défaut est créé
            Page(url=request.path).save()

    def process_response(self, request, response):
        """ Affiche le nombre de fois que la page a été vue """
        if response.status_code == 200:
            p = Page.objects.get(url=request.path)
            response.content += bytes(
                "Cette page a été vue {0} fois.".format(p.nb_visites), "utf8")
        return response

# Ici l'objet F permet de faire des requette directement en base de donnée (plus rapide)

# Attention normalement nous ne modifions pas le contenue de la réponse via un missleware !!