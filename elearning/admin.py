# elearning/admin.py
from django.contrib import admin
from .models import (
    CategorieModule, Module, Utilisateur, ModuleEnrollment,
    ContenuModule, ProgressionContenu, Quiz, Question, ChoixReponse,
    ReponseUtilisateur, ResultatQuiz, Certificat
)
from django.contrib.auth.admin import UserAdmin

# Enregistrement des modèles simples
admin.site.register(CategorieModule)
admin.site.register(ModuleEnrollment)
admin.site.register(ProgressionContenu)
admin.site.register(ReponseUtilisateur)
admin.site.register(ResultatQuiz)
admin.site.register(Certificat)


# Personnalisation de l'affichage du modèle Utilisateur dans l'admin
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {'fields': ('type_utilisateur', 'telephone', 'profession_medicale', 'niveau_acces', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {'fields': ('type_utilisateur', 'telephone', 'profession_medicale', 'niveau_acces', 'profile_picture')}),
    )
    list_display = UserAdmin.list_display + ('type_utilisateur', 'telephone', 'profession_medicale', 'profile_picture',)
    list_filter = UserAdmin.list_filter + ('type_utilisateur',)

admin.site.register(Utilisateur, CustomUserAdmin)

# Personnalisation pour Module et ContenuModule (pour l'admin en ligne)
class ContenuModuleInline(admin.TabularInline): # Ou admin.StackedInline pour un affichage différent
    model = ContenuModule
    extra = 1 # Nombre de formulaires vides à afficher
    # Si tu as un quiz lié à un ContenuModule, tu peux aussi l'inclure ici si tu le souhaites.
    # Par exemple:
    # inlines = [QuizInline]

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'niveau', 'createur', 'requiert_certification', 'date_creation')
    list_filter = ('categorie', 'niveau', 'requiert_certification')
    search_fields = ('titre', 'description')
    inlines = [ContenuModuleInline] # Permet de gérer les contenus directement depuis la page du module


# Personnalisation pour Quiz, Question, ChoixReponse (pour l'admin en ligne)
class ChoixReponseInline(admin.TabularInline):
    model = ChoixReponse
    extra = 3 # Afficher 3 choix vides par défaut
    min_num = 2 # Minimum de 2 choix par question

class QuestionInline(admin.StackedInline): # Ou TabularInline si tu préfères
    model = Question
    extra = 1
    inlines = [ChoixReponseInline]

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('titre', 'contenu_module', 'score_minimum', 'duree_limite_minutes')
    inlines = [QuestionInline]