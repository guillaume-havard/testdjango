from django.contrib import admin
from blog.models import Categorie, Article

# Register your models here.


#Pour pouvoir modifier l'affichage des ces models dans l'interface d'aministration
# Il faut créer des classes supplémentaires.
class ArticleAdmin(admin.ModelAdmin):
    list_display   = ('titre', 'categorie', 'auteur', 'date', 'apercu_contenu')
    list_filter    = ('auteur','categorie',)
    date_hierarchy = 'date'
    ordering       = ('date', )
    search_fields  = ('titre', 'contenu')
    
    # Permet de spécifier l'ordre des l'apparition des champs lors de la 
    # création d'un nouvel élément
    #fields = ('titre', 'slug', 'auteur', 'categorie', 'contenu')
    
    # Ordre avec des sous ensembles
    fieldsets = (
        # Fieldset 1 : meta-info (titre, auteur…)
        ('Général', {
            'classes': ['collapse',],
            'fields': ('titre', 'slug', 'auteur', 'categorie')
        }),
        # Fieldset 2 : contenu de l'article
        ('Contenu de l\'article', {
           'classes': ['wide',],
           'description': 'Le formulaire accepte les balises HTML. Utilisez-les à bon escient !',
           'fields': ('contenu', )
        }),
    )
   
    # Pour avoir un champ spécial
    def apercu_contenu(self, article):
        """ 
        Retourne les 40 premiers caractères du contenu de l'article. S'il
        y a plus de 40 caractères, il faut ajouter des points de suspension.
        """
        text = article.contenu[0:40]
        if len(article.contenu) > 40:
            return '%s...' % text
        else:
            return text
    # Pour que le champs spécial est une entête
    apercu_contenu.short_description = 'Aperçu du contenu'

    # Faire en sorte que le champs soit automatiquement remplit
    prepopulated_fields = {'slug': ('titre', ), }


# Il pourront ensuite ^etre modifié dans linterface d'administration.
admin.site.register(Categorie)
#admin.site.register(Article)
admin.site.register(Article, ArticleAdmin)
