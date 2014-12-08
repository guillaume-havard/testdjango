from django.contrib import admin
from blog.models import Categorie, Article

# Register your models here.


#Pour pouvoir modifier l'affichage des ces models dans l'interface d'aministration
# Il faut créer des classes supplémentaires.
class ArticleAdmin(admin.ModelAdmin):
   list_display   = ('titre', 'categorie', 'auteur', 'date')
   list_filter    = ('auteur','categorie',)
   date_hierarchy = 'date'
   ordering       = ('date', )
   search_fields  = ('titre', 'contenu')


# Il pourront ensuite ^etre modifié dans linterface d'administration.
admin.site.register(Categorie)
#admin.site.register(Article)
admin.site.register(Article, ArticleAdmin)