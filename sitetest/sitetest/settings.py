"""
Django settings for sitetest project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jvakg7q7x2gxwfkgrt2n_9k)a+2h#e0&^(pko1^^8*9x!mmwjj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'miniURL',
    'stats',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'stats.middleware.StatsMiddleware',

    'django.middleware.locale.LocaleMiddleware', #i18n
)

ROOT_URLCONF = 'sitetest.urls'

WSGI_APPLICATION = 'sitetest.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True # Mettre à false si pas utilisé, gain de place/temps.

USE_L10N = True

USE_TZ = True

# Fausse fonction gettext, permet de l'utiliser dans LANGUAGES, mais n'est pas importer
# Car fait partit de la configuration qui charge settings (ça ferait une boucle infinie)
gettext = lambda x: x

LANGUAGES = (
   ('fr', gettext('French')),
   ('en', gettext('English')),
)

## Pour l'internationalisation
# Il faut ajouter un middleware et contexte processor
# action du middleware
# Dans un premier temps, il est possible de configurer les URL pour les préfixer avec la langue voulue. Si ce préfixe apparaît, alors la langue sera forcée.
# Si aucun préfixe n'apparaît, le middleware vérifie si une langue est précisée dans la session de l'utilisateur.
# En cas d'échec, le middleware vérifie dans les cookies du visiteur si un cookie nommé _language (défini par Django) existe.
# En cas d'échec, il vérifie la requête HTTP et vérifie si l'en-tête Accept-Language est envoyé. Cet en-tête, envoyé par le navigateur du visiteur, spécifie les langues de prédilection, par ordre de priorité. Django essaie chaque langue une par une, selon celles disponibles dans notre projet.
# Enfin, si aucune de ces méthodes ne fonctionne, alors Django se rabat sur le paramètre LANGUAGE_CODE.

# Il y a deux modes de traduction différent d'nu coté les vues et models set l'autre les tempaltes.

# Une fois l'endroit des traduction faite il faut les écrire.
# Elles seront stockés dans des fichiers .po avec un langue par dossier
# Créer un dossier "locale"
# dans les app ou pour tout le projet

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Lancer la création des fichiers po avec
#python3 manage.py makemessages -l en
# MAIS ne fonctionne pas chez moi ...

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

#pour les images
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = MEDIA_ROOT

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",

    "sitetest.context_processors.get_infos",

    "django.core.context_processors.i18n", #i18n
)


### Les caches
# Définis grâce à la variable CACHE
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': '/var/tmp/django_cache',
#     }
# }
#'BACKEND' : méthode utilisé
#'LOCATION' : Lieu où enregistrer les données.

## Différentes méthodes
# Par les fichiers
#'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache'

# Dans la mémoire
#'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
# pas très efficace mais simple (par défaut)

# Dans une BdD
#'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#'LOCATION': 'nom_table_cache'
# IL faut créer une table avant
#python manage.py createcachetable [nom_table_cache]
# Pratique et rapide si serveur dédié, sinon pas forcement utile

# Avec MemCached (autre logiciel)
#'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#'LOCATION': '127.0.0.1:11211'
#Il faut installer le logiciel puis
#(console) memcached -d -m 512 -l 127.0.0.1 -p 11211
# Beaucoup plus efficace que ses pairs

# Cache de test (Ne fais rien)
#'BACKEND': 'django.core.cache.backends.dummy.DummyCache',

## Utilisation du cache

# Cache par vue
# from django.views.decorators.cache import cache_page
#
# @cache_page(60 * 15) # Durée du cache en seconde
# def lire_article(request, id):
#     article = Article.objects.get(id=id)
#     # ...

#Possible depuis les urls aussi :
# from django.views.decorators.cache import cache_page
#
# urlpatterns = ('',
#     (r'^article/(\d{1,4})/$', cache_page(60 * 15)(lire_article)),
# )

# Cache dans les tempalte
# {% load cache %}
# {% cache 500 carrousel %} # Tempen secondes
#     /* mon carrousel */
# {% endcache %}

# Il est possible d'avoir plusieurs copie d'un même template
# {% load cache %}
# {% cache 500 user.username %}
#     /* mon carrousel adapté à l'utilisateur actuel */
# {% endcache %}
# Par exemple ici l'utilisateur a sa copie

# Cache bas niveau
#from django.core.cache import cache
# cache.set('ma_cle', 'Coucou !', 30) # en secondes
# cache.get('ma_cle') -> 'Coucou !'

# cache.get('ma_cle', 'a expiré') # Deuxième argument, valeur par défaut si cache expiré.

# Pour plusieurs valeurs d'un coups:
# cache.set_many({'a': 1, 'b': 2, 'c': 3})
# cache.get_many(['a', 'b', 'c']) -> {'a': 1, 'b': 2, 'c': 3}

