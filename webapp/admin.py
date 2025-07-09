from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.db.models import Count



# Configuration de l'admin pour Utilisateur

class UtilisateurAdmin(UserAdmin):
    list_display = ['username', 'nom_complet', 'email', 'type_utilisateur', 'statut', 'est_verifie', 'date_joined']
    list_filter = ['type_utilisateur', 'statut', 'est_verifie', 'date_joined']
    search_fields = ['username', 'nom', 'prenom', 'email']
    readonly_fields = ['date_creation', 'date_modification', 'date_verification']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'telephone', 'date_naissance', 'adresse', 'ville', 'pays')
        }),
        ('Informations professionnelles', {
            'fields': ('type_utilisateur', 'etablissement', 'specialite', 'numero_ordre')
        }),
        ('Statut et validation', {
            'fields': ('statut', 'est_verifie', 'date_verification')
        }),
        ('Préférences', {
            'fields': ('langue_preference', 'notifications_email', 'notifications_sms')
        }),
    )
    
    actions = ['verifier_comptes', 'activer_comptes', 'desactiver_comptes']
    
    def nom_complet(self, obj):
        return f"{obj.prenom} {obj.nom}" if hasattr(obj, 'prenom') and hasattr(obj, 'nom') else obj.username
    nom_complet.short_description = 'Nom complet'
    
    def verifier_comptes(self, request, queryset):
        for utilisateur in queryset:
            if hasattr(utilisateur, 'verifier_compte'):
                utilisateur.verifier_compte()
        self.message_user(request, f"{queryset.count()} compte(s) vérifié(s).")
    verifier_comptes.short_description = "Vérifier les comptes sélectionnés"
    
    def activer_comptes(self, request, queryset):
        queryset.update(statut='actif')
        self.message_user(request, f"{queryset.count()} compte(s) activé(s).")
    activer_comptes.short_description = "Activer les comptes sélectionnés"


# Configuration pour CategorieModule

class CategorieModuleAdmin(admin.ModelAdmin):
    list_display = ['nom', 'nombre_modules', 'couleur_display', 'ordre', 'est_active']
    list_filter = ['est_active']
    search_fields = ['nom', 'description']
    list_editable = ['ordre', 'est_active']
    
    def nombre_modules(self, obj):
        return obj.module_set.count()
    nombre_modules.short_description = "Nb modules"
    
    def couleur_display(self, obj):
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            obj.couleur, obj.couleur
        )
    couleur_display.short_description = "Couleur"






class ModuleAdmin(admin.ModelAdmin):
    list_display = ['titre', 'categorie', 'createur', 'niveau', 'statut', 'nombre_inscriptions', 'note_moyenne', 'date_creation']
    list_filter = ['statut', 'niveau', 'categorie', 'est_gratuit', 'est_certifiant']
    search_fields = ['titre', 'description']
    readonly_fields = ['uuid', 'slug', 'nombre_vues', 'nombre_inscriptions', 'note_moyenne']
  
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('titre', 'slug', 'description_courte', 'description', 'categorie', 'createur')
        }),
        ('Caractéristiques', {
            'fields': ('niveau', 'type_module', 'duree_estimee', 'points_xp', 'prerequis')
        }),
        ('Média', {
            'fields': ('image_couverture', 'video_intro')
        }),
        ('Publication', {
            'fields': ('statut', 'est_gratuit', 'prix', 'est_certifiant')
        }),
        ('Statistiques', {
            'fields': ('nombre_vues', 'nombre_inscriptions', 'note_moyenne'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['publier_modules', 'archiver_modules']
    
    def publier_modules(self, request, queryset):
        for module in queryset:
            if hasattr(module, 'publier'):
                module.publier()
        self.message_user(request, f"{queryset.count()} module(s) publié(s).")
    publier_modules.short_description = "Publier les modules sélectionnés"


# Configuration pour Contenu

class ContenuAdmin(admin.ModelAdmin):
    list_display = ['titre', 'module', 'type_contenu', 'ordre', 'duree_display', 'est_obligatoire']
    list_filter = ['type_contenu', 'est_obligatoire', 'est_gratuit']
    search_fields = ['titre', 'module__titre']
    list_editable = ['ordre']
    
    def duree_display(self, obj):
        if obj.duree:
            minutes = obj.duree // 60
            secondes = obj.duree % 60
            return f"{minutes}:{secondes:02d}"
        return "-"
    duree_display.short_description = "Durée"
