from django.db import models


"""
Acceder aux element du modèle
from blog.models import Article # pensez à incure le modèle
Sauvegarder un element : element.save()
le supprimer element.delete()


Renvoie des QuerySet (ensemble de réponses) :
Article.objects.all()

Article.objects.filter(auteur="Maxime"):
Article.objects.exclude(auteur="Maxime"):
Article.objects.filter(titre__contains="crêpe")
Après le champ et les deux "__" il peut avoir plusieurs mots clefs:
lt gt lte gte ...
Article.objects.order_by('date')
Article.objects.order_by('-date')
#Cumul de plusieurs requettes :
Article.objects.filter(date__lt=datetime.now()).order_by('date','titre').reverse()
# Ne recupèreque s'il y a 1 réponse, sinon erreur
Article.objects.get(titre="Je n'existe pas") -> DoesNotExist: Article matching query does not exist.
Lookup parameters were {'titre': "Je n'existe pas"}
>>> Article.objects.get(titre__contains="test"). -> requette ok
>>> Article.objects.get(titre__contains="L") -> MultipleObjectsReturned: get() returned more than one Article
-- it returned 2! Lookup parameters were {'titre__contains': 'L'}
# Cherche un article comme get le cré s'il n'existe pas
Article.objects.get_or_create(auteur="Jean-René")
retourn un tuple avec l'article (comme get) et un booleen s'il a crée l'aricle ou pas.

# avec Categorie exemple d'utilisation de clefs étrangères pour Article
SI l'on veut, depuis une catégorie, retrouver les elements d'une table qui lui sont lié il suffit de faire

cat.article_set.all() # ou toute autre commandes vu avec objects
#La nouvelle classe (article_set) est composée d'une nom de la table avec la clef etrangère de '_' et de set.

Il est aussi possible de faire des recherche pour une Categorie via un Article
#Article.objects.filter(categorie__nom__contains="test")

Avec VOiture et Moteur exemple de lien unique :
#Pour acceder au moteur de la voiture on fait
voiture.moteur
#mais il est aussi possible de faire:
moteur.voiture
# Un peut comme article_set sauf que là vu que la connection est unique le "_set" n'est pas nécessaire.

# Pour les deux cas de "relation inverse" il est possible de le spécifier lors de la creation de la clef ou du oneToOne
avec l'argument "related_name". Il est aussi possible de le désactiver avec related_name='+'.


#Dernier exemple de lien ManyToMany:
Produit, Vendeur Offre
Vendeur.manytomany (Produit)   ici Vendeur = source

Le many to many créer une table supplémentaire automatiquement ici elle est spécifiée
étant donné que l'on veut ajouter un prix.

#Pour créer une offre manuellement crer un element avec les bonnes clef étrangère
#si automatique :
vendeur.produits.add(p1,p2)
#Pour la supprimer manuellement, supprimer l'entrée dans la tble
#si automatique :
vendeur.produits.remove(p1) # Nous avons supprimé p1, il ne reste plus que p2 qui est lié au vendeur

#Pour acceder aux Produit
vendeur.produits.all()
# Pour y acceder au relation inverse :
p1.vendeur_set.all()

#Pour tout supprimer sur la table intermédiaire (man. ou auto.):
vendeur.produits.clear()


"""


# Create your models here.
class Article(models.Model):
    titre = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    auteur = models.CharField(max_length=42)
    contenu = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name="Date de parution")
    categorie = models.ForeignKey('Categorie')
    nb_vues = models.IntegerField(default=0)

    def est_recent(self):
        """ Retourne True si l'article a été publié dans
            les 30 derniers jours """
        from datetime import datetime
        return (datetime.now() - self.date).days < 30  and self.date < datetime.now()

    def __str__(self):
        """
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que
        nous traiterons plus tard et dans l'administration
        """
        return self.titre

class Categorie(models.Model):
    nom = models.CharField(max_length=30)

    def __str__(self):
        return self.nom

class Moteur(models.Model):
    nom = models.CharField(max_length=25)

    def __str__(self):
        return self.nom

class Voiture(models.Model):
    nom = models.CharField(max_length=25)
    moteur = models.OneToOneField(Moteur)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    nom = models.CharField(max_length=30)

    def __str__(self):
        return self.nom

class Vendeur(models.Model):
    nom = models.CharField(max_length=30)
    produits = models.ManyToManyField(Produit, through='Offre')

    def __str__(self):
        return self.nom

class Offre(models.Model):
    prix = models.IntegerField()
    produit = models.ForeignKey(Produit)
    vendeur = models.ForeignKey(Vendeur)

    def __str__(self):
        return "{0} vendu par {1}".format(self.produit, self.vendeur)

class Contact(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.TextField()
    photo = models.ImageField(upload_to="photos/")
    
    def __str__(self):
           return self.nom

    
# Pour donner des noms spécifiques aux fichiers
def renommage(instance, nom):
    nom_fichier = os.path.splitext(nom)[0] # on retire l'extension
    return "{}-{}".format(instance.id, nom_fichier)
    
# Documents (fichier) avec nom prenant en compte l'id en BdD.
class Document(models.Model):
    nom = models.CharField(max_length=100)
    doc = models.FileField(upload_to=renommage, verbose_name="Document")


## ALLEZ plus lion avec les modèles
class Eleve(models.Model):
    nom = models.CharField(max_length=31)
    moyenne = models.IntegerField(default=10)

    def __str__(self):
        return "Élève {0} ({1}/20 de moyenne)".format(self.nom, self.moyenne)

## Q
# from django.db.models import Q
#Eleve.objects.filter(Q(nom="Maxime"))
# Meme résulatat que :
#Eleve.objects.filter(nom="Maxime")
# Mais avec Q im est possible de faire :
#Eleve.objects.filter(Q(moyenne__gt=16) | Q(moyenne__lt=8))
# ou
#Eleve.objects.filter(Q(moyenne=10) & Q(nom="Sofiane"))
#Eleve.objects.filter(Q(moyenne=10), Q(nom="Sofiane")) ',' pareil que '&'
# inversion avec '~'
#Eleve.objects.filter(Q(moyenne=10), ~Q(nom="Sofiane"))
# requette Q "Q(('moyenne',10))" pareil que "Q(moyenne=10)"
#conditions = [('moyenne', 15), ('nom', 'Thibault'), ('moyenne', 18)]
#objets_q = [Q(x) for x in conditions]
#import operator
#Eleve.objects.filter(reduce(operator.or_, objets_q))

## Les agrégations
# Opération mathématiques sur des elements du modèle
#from django.db.models import Avg
#Eleve.objects.aggregate(Avg('moyenne'))
# le resultat est un dictionnaire avec le nom donne suivi de l'opération comme clef
#res : {'moyenne__avg': 11.25}
# Les opération peuvent etre combinées
#Eleve.objects.aggregate(Avg('moyenne'), Min('moyenne'), Max('moyenne'), Count('moyenne'))
#{'moyenne__max': 18, 'moyenne__avg': 11.25, 'moyenne__min': 7, 'moyenne__cnt': 4}
# Spécification des clefs
#Eleve.objects.aggregate(Moyenne=Avg('moyenne'), Minimum=Min('moyenne'), Maximum=Max('moyenne'), Nombre=Count('moyenne'))
#{'Minimum': 7, 'Moyenne': 11.25, 'Maximum': 18, 'Nombre': 4}

## Annotation
#Rajouter un champs dans l'objet
#Cours.objects.annotate(Avg("eleves__moyenne"))[0].eleves__moyenne__avg # contient 11.25
#Cours.objects.annotate(Moyenne=Avg("eleves__moyenne"))[1].Moyenne # pareil, 12.5
#Cours.objects.annotate(Moyenne=Avg("eleves__moyenne")).filter(Moyenne__gte=12) # -> [<Cours: Anglais>]

## héritage des modèles
# 3 méthode d'héritage avec Django
#-- Les modèles parents abstraits
# 1 modèle de badse abstrait (pas de modèle en base de données) pourra servir de base pour d'autres modèles
# classe abstratire : surcharge Meta avec "abstract = True"
# class Document(models.Model):
#     titre = models.CharField(max_length=255)
#     date_ajout = models.DateTimeField(auto_now_add=True,
#                                       verbose_name="Date d'ajout du document")
#     auteur = models.CharField(max_length=255, null=True, blank=True)
#
#     class Meta:
#         abstract = True
#
# class Article(Document):
#     contenu = models.TextField()
#
# class Image(Document):
#     image = models.ImageField(upload_to="images"

# Aucune manipulation est possible avec le modèle abstrait


#-- Les modèles parents classiques
# class Lieu(models.Model):
#     nom = models.CharField(max_length=50)
#     adresse = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.nom
#
# class Restaurant(Lieu):
#     menu = models.TextField()

# Lieu peut exister seul ainsi que Restaurant
# Cependant lorsqu'un restaurant est créé la partie correspondant au lieu sera ajouté dans la table Lieu
# dans Restaurant il y aur le menu ansi qu'une FK pour l'a bonne entrée dans Lieu.

# il est possible d'acdeser à un classe fille depuis la classe d'origine, il suffit de donner le nom de cette classe
#print type(lieu.restaurant) # -> <class 'blog.models.Restaurant'>

#-- Les modèles proxy
# Le modèle fille ne sera pas en basse de donnée
# il permet d'avoir un acces et des manipulation de données différente que sa classe mère mais avec les meme données
# class RestoProxy(Restaurant):
#     class Meta:
#         proxy = True  # Nous spécifions qu'il s'agit d'un proxy
#         ordering = ["nom"]  # Nous changeons le tri par défaut
#
#     def crepes(self):
#         if "crêpe" in self.menu:  # Il y a des crêpes dans le menu
#             return True
#         return False

# Que ce soit par Restaurant ou Resto proxy nous aurons les m^eme données.
# Mais avec RestoProxi il est possible de savoir s'il y a des cr^epes au menu.

## ContentTypes
# permet le lien d'une entrée de modèle à un autre modèle ...
# Attention i doit ^etre dans les INSTALLED_APPS 'django.contrib.contenttypes'

#from blog.models import Eleve
#from django.contrib.contenttypes.models import ContentType
#ct = ContentType.objects.get(app_label="blog", model="eleve")  # ct -> <ContentType: eleve>

#ContentType a deux méthodes qui lui sont propre
# model class renvoie la classe du modèle représenté
# get_object_for_this_type raccourci pour model_class().objects.get(attr=arg)

#ct.model_class() # -> <class 'blog.models.Eleve'>
#ct.get_object_for_this_type(nom="Maxime") # -> <Eleve: Élève Maxime (7/20 de moyenne)>

# en faisant :
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes.fieds import GenericForeignKey
#
# class Commentaire(models.Model):
#     auteur = models.CharField(max_length=255)
#     contenu = models.TextField()
#     content_type = models.ForeignKey(ContentType)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
#
#     def __str__(self):
#         return "Commentaire de {0} sur {1}".format(self.auteur, self.content_object)

# la "vrai" clef etrangère est sonstitué d'une d'une clef et d'une reférene vers un modèle pour le moment inconu
# qui devra ^etre renseigner à la création de l'entrée Commentaire.

# from blog.models import Commentaire, Eleve
# e = Eleve.objects.get(nom="Sofiane")
# c = Commentaire.objects.create(auteur="Le professeur",contenu="Sofiane ne travaille pas assez.", content_object=e)
# c.content_object -> <Eleve: Élève Sofiane (10/20 de moyenne)>
# c.object_id -> 4
# c.content_type.model_class() -> <class 'blog.models.Eleve'>

# /!\ dans ce cas plus de relation inverse possible nativement

# Il faudra rajouter un champs dans le modèle reféré
# ici Elève :
#    commentaires = GenericRelation('Commentaire')
# attention si vous avez changer les noms "content_type" et "object_id" pour la clef etrangère
# vous devez spécifier ces noms :

# commentaires = GenericRelation(Commentaire,
#     content_type_field="le_champ_du_content_type",
#     object_id_field="le champ_de_l_id")


### Les Signaux
# Moyen de communiquer avec l'ensemble du projet

# def ma_fonction_de_suppression(sender, instance, **kwargs):
# 	# processus de suppression selon les données fournies par instance
# from django.models.signals import post_delete
# post_delete.connect(ma_fonction_de_suppression, sender=MonModele)

# Chaque fois qu'un post du modele MonModele est supprimé la fonction "ma_fonction_de_suppression" est appelée.

# Pareil en plus rapide :
# from django.models.signals import post_delete
# from django.dispatch import receiver
# @receiver(post_delete, sender=MonModele)
# def ma_fonction_de_suppression(sender, instance, **kwargs):
# 	# processus de suppression selon les données fournies par instance

# Il existe d'autre signaux que post_delete (https://docs.djangoproject.com/en/1.7/ref/signals/) avec des argument différents
# il es possible de faire ses propres signaux

### Les middlewares
        # Interviennent juste avant et après l'apple de la vue, permettent de faire des actions sur les données.
# Il en existe déjà, voir settings.py MIDDLEWARE_CLASSES

# exemple
# process_request(self, request) : à l'arrivée d'une requête HTTP, avant de la router vers une vue précise. request est un objet HttpRequest (le même que celui passé à une vue).
# process_view(self, request, view_func, view_args, view_kwargs) : juste avant d'appeler la vue. view_func est une référence vers la fonction prête à être appelée par le framework.
# view_args et view_kwargs sont les arguments prêts à être appelés avec la vue.
# process_template_response(self, request, response) : lorsque le code retourne un objet TemplateResponse d'une vue. response est un objet HttpResponse (celui retourné par la vue appelée).
# process_response(self, request, response) : juste avant que Django renvoie la réponse.
# process_exception(self, request, exception) : juste avant que Django renvoie une exception si une erreur s'est produite. exception est un objet de type Exception.

# SDZ : les middlewares sont appelés dans l'ordre précisé dans le setting.py, de haut en bas, pour toutes les méthodes appelées avant l'appel de la vue
# (soit process_request et process_view). Après, les middlewares sont appelés dans le sens inverse, de bas en haut
# voir : http://sdz-upload.s3.amazonaws.com/prod/upload/middlewares-exec.png

# Voir l'application 'stats'.


## Internationalisation
# semblable aux vues sauf qu'il faut ajouter '_lazy' aux noms des fonctions.
# Comme ça la traduction n'est faite qu'à l'affichage et no pendant l'enregistrement