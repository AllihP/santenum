from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Module, CategorieModule, Utilisateur # Assure-toi que ces modèles sont bien importés
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




# --- Vue pour lister tous les modules ---
@login_required # S'assure que seul un utilisateur connecté peut accéder à cette vue
def liste_modules(request):
    """
    Affiche la liste de tous les modules de formation.
    Permet de filtrer par catégorie et de rechercher par titre.
    """
    modules = Module.objects.all()
    categories = CategorieModule.objects.all()
    
    # Filtrage par catégorie
    categorie_id = request.GET.get('categorie')
    if categorie_id:
        modules = modules.filter(categorie__id=categorie_id)

    # Recherche par titre
    query = request.GET.get('q')
    if query:
        modules = modules.filter(titre__icontains=query) # icontains pour recherche insensible à la casse

    # Pagination
    paginator = Paginator(modules, 10) # 10 modules par page
    page_number = request.GET.get('page')
    try:
        modules_pagines = paginator.page(page_number)
    except PageNotAnInteger:
        # Si le paramètre page n'est pas un entier, afficher la première page.
        modules_pagines = paginator.page(1)
    except EmptyPage:
        # Si la page est hors de portée (e.g. 9999), afficher la dernière page de résultats.
        modules_pagines = paginator.page(paginator.num_pages)

    context = {
        'modules': modules_pagines,
        'categories': categories,
        'selected_category_id': categorie_id,
        'search_query': query,
    }
    return render(request, 'learning_modules/liste_modules.html', context)

# --- Vue pour afficher les détails d'un module spécifique ---
@login_required
def detail_module(request, module_id):
    """
    Affiche les détails d'un module de formation spécifique.
    """
    module = get_object_or_404(Module, id=module_id)
    
    # Ici, tu pourrais ajouter de la logique pour :
    # - Récupérer les contenus liés au module
    # - Vérifier la progression de l'utilisateur sur ce module
    # - Afficher les certifications si complétées

    context = {
        'module': module,
        # 'contenus_module': module.contenus.all(), # Si tu as un champ related_name='contenus' dans ton modèle Contenu
    }
    return render(request, 'learning_modules/detail_module.html', context)


# --- Vue pour un tableau de bord par type d'utilisateur ---
@login_required
def tableau_de_bord(request):
    """
    Affiche un tableau de bord personnalisé selon le type d'utilisateur.
    """
    user_type = request.user.type_utilisateur
    modules_recommandes = []
    
    if user_type == 'medecin':
        # Exemple: recommander des modules de téléconsultation
        modules_recommandes = Module.objects.filter(
            categorie__nom='Consultation', 
            niveau__in=['debutant', 'intermediaire']
        ).order_by('?')[:5] # Ordre aléatoire pour la recommandation
    elif user_type == 'technicien':
        # Exemple: recommander des modules sur les équipements
        modules_recommandes = Module.objects.filter(
            categorie__nom='Équipements',
            niveau__in=['debutant', 'intermediaire']
        ).order_by('?')[:5]
    # ... ajoutez d'autres conditions pour les autres types d'utilisateurs

    context = {
        'user_type': user_type,
        'modules_recommandes': modules_recommandes,
        # Tu peux ajouter ici des données de progression de l'utilisateur, etc.
    }
    return render(request, 'learning_modules/tableau_de_bord.html', context)


@login_required # Pour s'assurer que seuls les utilisateurs connectés voient le dashboard
def home_page(request):
    """
    Redirige vers le tableau de bord si l'utilisateur est connecté,
    sinon vers la page de connexion.
    """
    # Tu pourrais aussi afficher une page d'accueil statique ici si l'utilisateur n'est pas connecté
    # Pour l'instant, on redirige juste vers le tableau de bord pour les connectés
    return redirect(reverse('elearning:tableau_de_bord'))

# Ou une page d'accueil générique si tu préfères
# def welcome_page(request):
#     return render(request, 'elearning/welcome.html')

@login_required
def mon_profil(request):
    """
    Affiche la page de profil de l'utilisateur connecté.
    """
    user_profile = request.user
    context = {
        'user_profile': user_profile,
          # Assure-toi que ce
    }
    return render(request, 'elearning/profil.html', context)

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})


@login_required
def detail_module(request, module_id):
    """
    Affiche les détails d'un module spécifique, y compris ses contenus.
    """
    module = get_object_or_404(Module, pk=module_id)
    # Récupérer les contenus du module, ordonnés par le champ 'ordre'
    contenus = module.contenus.all().order_by('ordre')

    # Si vous voulez afficher la progression de l'utilisateur pour chaque contenu
    user_progress = {}
    if request.user.is_authenticated:
        for contenu in contenus:
            # Tente de récupérer la progression, sinon met False
            progress, created = ProgressionContenu.objects.get_or_create(
                user=request.user,
                contenu_module=contenu
            )
            user_progress[contenu.id] = progress.completed

    context = {
        'module': module,
        'contenus': contenus,
        'user_progress': user_progress, # Passer la progression au template
    }
    # C'est ici que le chemin du template doit être corrigé
    return render(request, 'elearning/detail_module.html', context)

# --- Vue pour lister tous les modules ---
@login_required # S'assure que seul un utilisateur connecté peut accéder à cette vue
def liste_modules(request):
    """
    Affiche la liste de tous les modules de formation.
    Permet de filtrer par catégorie et de rechercher par titre.
    """
    modules = Module.objects.all()
    categories = CategorieModule.objects.all()

    # Filtrage par catégorie
    categorie_id = request.GET.get('categorie')
    if categorie_id:
        modules = modules.filter(categorie__id=categorie_id)

    # Recherche par titre
    query = request.GET.get('q')
    if query:
        modules = modules.filter(titre__icontains=query) # icontains pour recherche insensible à la casse

    # Pagination
    paginator = Paginator(modules, 10) # 10 modules par page
    page_number = request.GET.get('page')
    try:
        modules_pagines = paginator.page(page_number)
    except PageNotAnInteger:
        # Si le paramètre page n'est pas un entier, afficher la première page.
        modules_pagines = paginator.page(1)
    except EmptyPage:
        # Si la page est hors de portée (e.g. 9999), afficher la dernière page de résultats.
        modules_pagines = paginator.page(paginator.num_pages)

    context = {
        'modules': modules_pagines,
        'categories': categories,
        'selected_category': categorie_id, # Pour maintenir la catégorie sélectionnée dans le formulaire
        'query': query, # Pour maintenir le terme de recherche dans le formulaire
    }
    # C'est ici que le chemin du template doit être corrigé
    return render(request, 'elearning/liste_modules.html', context)


@login_required # Pour s'assurer que seuls les utilisateurs connectés voient le dashboard
def tableau_de_bord(request):
    """
    Affiche le tableau de bord de l'utilisateur avec des modules recommandés
    en fonction de son type d'utilisateur.
    """
    user = request.user
    user_type = user.type_utilisateur
    modules_recommandes = []

    # Exemple de logique de recommandation basée sur le type d'utilisateur
    # Adaptez cette logique à vos besoins réels
    if user_type == 'medecin':
        modules_recommandes = Module.objects.filter(
            categorie__nom__in=['Télémédecine', 'Diagnostic', 'Thérapeutique'],
            niveau__in=['debutant', 'intermediaire', 'avance']
        ).order_by('?')[:5] # Affiche 5 modules aléatoires

    elif user_type == 'technicien':
        modules_recommandes = Module.objects.filter(
            categorie__nom='Équipements',
            niveau__in=['debutant', 'intermediaire']
        ).order_by('?')[:5]
    # ... ajoutez d'autres conditions pour les autres types d'utilisateurs

    context = {
        'user_type': user_type,
        'modules_recommandes': modules_recommandes,
        # Tu peux ajouter ici des données de progression de l'utilisateur, etc.
    }
    # C'est ici que le chemin du template doit être corrigé
    return render(request, 'elearning/tableau_de_bord.html', context)
