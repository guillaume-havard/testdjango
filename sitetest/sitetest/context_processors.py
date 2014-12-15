from datetime import datetime

# Ce fichier doit être ajouté à la variable TEMPLATE_CONTEXT_PROCESSORS de settings.py
# !!!! Django utilise déjà cette variable mais elle n'est pas affiché dans le fichier settings.py de base
"""
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
)
"""

def get_infos(request):
    date_actuelle = datetime.now()
    return {'date_actuelle': date_actuelle}

# /!\ aux noms des clefs, ils doivent être différent de ceux retournés par les vue sinon elles seront ecrasées.

# /!\ les fonction de retour de vue ne font pas tout le temps l'appele au contexte
# (render est un raccourci faisant plusieurs chose dont la récupération du contexte
# il faudra doc l'ajouter spécifiquement pour certaine fonction

#return render_to_response('blog/archives.html', locals(), context_instance=RequestContext(request))