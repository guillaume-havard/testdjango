from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

# L'application doit être dans les INSTALLED_APPS

# Pour ce que l'on fasse soit pris en compte pour les templates.
register = template.Library()

# Une fois que les rajout seront implémenter il suffit de mettre {% load blog_extras %} dans un template pour les utiliser
# ({% load blog_extras static i18n %})
# Tous les fichiers tempaltetags sont dans le même espace de nomage !!

### Filtres
#exemple
# Filtre upper sur la variable "texte" :
# {{ texte|upper }}
#
# Filtre truncatewords, avec comme argument "80" sur la variable "texte" :
# {{ texte|truncatewords:80 }}
#
# def citation(texte):
#     """
#     Affiche le texte passé en paramètre, encadré de guillemets
#     français doubles et d'espaces insécables
#     """
#     return "«&nbsp;%s&nbsp;»" % texte

# Pour enregistrer la fonction pour qu'elle puisse être utilisée dans un templeta
# Il est possible d'utiliser des décorateur ou une focntion de register (template.Library())

# @register.filter
# def citation1(texte):
#     return "«&nbsp;%s&nbsp;»" % texte
#
# @register.filter(name='mon_filtre_citation')
# def citation2(texte):
#     return "«&nbsp;%s&nbsp;»" % texte
#
# def citation3(texte):
#     return "«&nbsp;%s&nbsp;»" % texte
#
# register.filter('un_autre_filtre_citation', citation3)

# /!\ de base Django echape tous les charactères spéiau et les résultats de filtres
# Pour dire que notre chaine est sur rajouter l'argument is_safe=True au moment de l'ajout de la fonction.
# @register.filter(is_safe=True)
# def citation(texte):
#     """
#     Affiche le texte passé en paramètre, encadré de guillemets
#     français doubles et d'espaces insécables
#     """
#     return "« %s »" % texte

# /!\ si le code vient de l'exterieur nous ne sommes pas sur que le code soit sur.

@register.filter(is_safe=True)
def citation(texte):
    """
    Affiche le texte passé en paramètre, encadré de guillemets
    français doubles et d'espaces insécables.
    """
    res = "«&nbsp;%s&nbsp;»" % escape(texte)
    return mark_safe(res)

# EN faisant ansi nous echapons le texte utilisateur nous rajoutons nos charactère spéiaux puis nous marquons le tout safe.

## Filtre avec arguments
@register.filter
def smart_truncate(texte, nb_caracteres=20):
    """
    Coupe la chaîne de caractères jusqu'au nombre de caractères souhaité,
    sans couper la nouvelle chaîne au milieu d'un mot.
    Si la chaîne est plus petite, elle est renvoyée sans points de suspension.
    ---
    Exemple d'utilisation :
    {{ "Bonjour tout le monde, c'est Diego"|smart_truncate:18 }} renvoie
    "Bonjour tout le..."
    """

    # Nous vérifions tout d'abord que l'argument passé est bien un nombre
    try:
           nb_caracteres = int(nb_caracteres)
    except ValueError:
           return texte  # Retour de la chaîne originale sinon

    # Si la chaîne est plus petite que le nombre de caractères maximum voulus,
    # nous renvoyons directement la chaîne telle quelle.
    if len(texte) <= nb_caracteres:
           return texte

    # Sinon, nous coupons au maximum, tout en gardant le caractère suivant
    # pour savoir si nous avons coupé à la fin d'un mot ou en plein milieu
    texte = texte[:nb_caracteres + 1]

    # Nous vérifions d'abord que le dernier caractère n'est pas une espace,
    # autrement, il est inutile d'enlever le dernier mot !
    if texte[-1:] != ' ':
           mots = texte.split(' ')[:-1]
           texte = ' '.join(mots)
    else:
           texte = texte[0:-1]

    return texte + '…'

### Les contextes de templates
# rappel contexte : ensemble des données disponibles dans notre template
# si l'on fait return render(request, 'blog/archives.html', {'news': news, 'date': date_actuelle})
# news et date son incorporées au contexte d'archive.html

# Voir sitetest/context_processors.py