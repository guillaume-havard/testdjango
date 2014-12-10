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
