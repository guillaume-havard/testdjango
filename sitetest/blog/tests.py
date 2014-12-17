from django.test import TestCase
from datetime import datetime, timedelta
from blog.models import Article

# Django traitera tous les fichier sui commencent par "test"

# Create your tests here.



class ArticleTests(TestCase):
    fixtures = ['test_BdD.json']
    def test_est_recent_avec_futur_article(self):
        """
        Vérifie si la méthode est_recent d'un Article ne
        renvoie pas True si l'Article a sa date de publication
        dans le futur.
        """

        futur_article = Article(date=datetime.now() + timedelta(days=20))
        # Il n'y a pas besoin de remplir tous les champs, ni de sauvegarder
        self.assertEqual(futur_article.est_recent(), False)

# Plusieurs types d'asserts :
# assertEqual(a, b) <=> a == b
# assertTrue(x) <=> bool(x) is True
# assertFalse(x) <=> bool(x) is False
# assertIs(a, b) <=> a is b
# assertIsNone(x) <=> x is None
# assertIn(a, b) <=> a in b
# assertIsInstance(a, b) <=> isinstance(a, b)

## Pour lancer les tests
#python3 manage.py test
# Il est possible de préciser un fichier/class/test pour lancer les tests
#python manage.py test blog.tests

## Données des tests
#Django n'utilise pas les BdD pour les test.
# Nous pouvons utiliser des 'fixtures' pour initialiser nos données.

# Pour cela il est possible de "dumper" la BdD (enregistrer sous un autre format)
#python3 manage.py dumpdata blog
# Puis enregistrerles données dans un fichier de l'application et le donner en entré des tests
# cf fixtures = ['test_BdD.json'] dans ArticleTests

# La seconde méthode est d'avoir une méthode d'initilisation qui s'appelle 'setUp'.
class UnTest(TestCase):
    def setUp(self):
        self.une_variable = "Salut !"

    def test_verification(self):
        self.assertEqual(self.une_variable, "Salut !")

## Le module de test permet aussi de tester les vue.
#Il contient un petit serveur web pour tester les vue (dont les formulaires)