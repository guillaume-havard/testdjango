from django import forms

class ContactForm(forms.Form):
    sujet = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    envoyeur = forms.EmailField(label="Votre adresse mail")
    renvoi = forms.BooleanField(help_text="Cochez si vous souhaitez obtenir une copie du mail envoyé.", required=False)

    # Pour vérifier un champs
    # doit dommencer par "clean_" puis continuer avec le nom de la variable à vérifier.
    # est appelé après le Form.cleaned_data
    """
    def clean_message(self):
        message = self.cleaned_data['message']
        if "pizza" in message:
            raise forms.ValidationError("On ne veut pas entendre parler de pizza !")

        return message  # Ne pas oublier de renvoyer le contenu du champ traité
    """

    # Pour vérifier plusieurs champs entre eux il faut surcharger la méthode clean.
    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        sujet = cleaned_data.get('sujet')
        message = cleaned_data.get('message')

        if sujet and message:  # Est-ce que sujet et message sont valides ?
            if "pizza" in sujet and "pizza" in message:
                # Erreur général en haut du formulaire
                #raise forms.ValidationError("Vous parlez de pizzas dans le sujet ET le message ? Non mais ho !")
                # Pour l'avoir sur le bon champs :
                msg = "Vous parlez déjà de pizzas dans le sujet, n'en parlez plus dans le message !"
                #self.add_error("message", msg)
                # ou
                self.add_error("message",
                               forms.ValidationError("Vous parlez de pizzas dans le sujet ET le message ? Non mais ho !"))

        return cleaned_data  # N'oublions pas de renvoyer les données si tout est OK