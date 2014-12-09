from django import forms
from miniURL.models import Redirection


#Pour faire un formulaire depuis un modèle. (/!\ héritage différent)
class RedirectionForm(forms.ModelForm):
    class Meta:
        model = Redirection
        fields = ('real_url', 'pseudo')

# Pour récupérer des données cel apeut ce faire avec un POST
# ou directement en donnant un objet du modele :
#form = ArticleForm(instance=article)  # article est bien entendu un objet d'Article quelconque dans la base de données
# Le champs est ainsi préremplit.

# Quand on a recu une bonne formeModele il suffit de save() pour la mettre en base