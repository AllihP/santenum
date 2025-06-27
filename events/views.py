# events/views.py

from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta # Import correct
from django.utils.translation import gettext_lazy as _ # Pour les messages, si besoin

from .models import Event, EventCategory, Location # Assurez-vous d'importer tous les modèles nécessaires
from .forms import EventSearchForm # Importez le formulaire de recherche

class EventListView(ListView):
    model = Event
    template_name = 'events/evenements.html'
    context_object_name = 'events'
    paginate_by = 12
    # self.filter est supprimé car le filtrage est maintenant géré uniquement par le formulaire

    def get_queryset(self):
        # Toujours commencer avec les événements publiés
        queryset = Event.objects.filter(status='PUBLISHED').select_related(
            'category', 'location', 'organizer'
        ).prefetch_related('partners')

        form = EventSearchForm(self.request.GET) # Initialise le formulaire avec les données GET

        if form.is_valid():
            cleaned_data = form.cleaned_data
            search_query = cleaned_data.get('search')
            category = cleaned_data.get('category')
            location_city = cleaned_data.get('location_city')
            location_region = cleaned_data.get('location_region')
            event_type = cleaned_data.get('event_type')
            date_filter = cleaned_data.get('date_filter')
            sort_by = cleaned_data.get('sort_by')
            is_online = cleaned_data.get('is_online') # Récupérer le champ is_online

            # Appliquer les filtres basés sur le formulaire validé
            if search_query:
                queryset = queryset.filter(
                    Q(title__icontains=search_query) |
                    Q(description__icontains=search_query) |
                    Q(target_audience__icontains=search_query)
                )
            if category:
                queryset = queryset.filter(category=category)
            if location_city:
                queryset = queryset.filter(location__city=location_city)
            if location_region:
                queryset = queryset.filter(location__region=location_region)
            if event_type:
                queryset = queryset.filter(type=event_type)

            today = timezone.now().date() # Utiliser .date() pour les comparaisons de dates strictes

            if date_filter == 'upcoming':
                queryset = queryset.filter(end_date__gte=timezone.now())
            elif date_filter == 'ongoing':
                queryset = queryset.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now())
            elif date_filter == 'past':
                queryset = queryset.filter(end_date__lt=timezone.now())
            elif date_filter == 'today':
                queryset = queryset.filter(
                    start_date__year=today.year,
                    start_date__month=today.month,
                    start_date__day=today.day
                )
            elif date_filter == 'this_week':
                # today.weekday() retourne 0 pour lundi, 6 pour dimanche
                start_of_week = today - timedelta(days=today.weekday())
                end_of_week = start_of_week + timedelta(days=6)
                # Utiliser __date pour comparer seulement la date, ignorer l'heure
                queryset = queryset.filter(start_date__date__range=[start_of_week, end_of_week])
            elif date_filter == 'this_month':
                queryset = queryset.filter(start_date__year=today.year, start_date__month=today.month)
            
            # Filtre pour événement en ligne (is_online)
            # NullBooleanField renvoie True, False ou None. is not None est la bonne approche.
            if is_online is not None:
                queryset = queryset.filter(is_online=is_online)

            # Appliquer le tri
            if sort_by:
                queryset = queryset.order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passe une instance du formulaire à la vue, remplie avec les données GET si présentes
        context['search_form'] = EventSearchForm(self.request.GET)
        # Il peut être utile de passer toutes les catégories si elles sont utilisées pour autre chose que le formulaire
        context['event_categories'] = EventCategory.objects.filter(is_active=True).order_by('name')
        # context['current_filter'] n'est plus nécessaire si le formulaire gère tout
        return context