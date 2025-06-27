# events/forms.py

from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Event, EventCategory, Location

class EventSearchForm(forms.Form):
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Rechercher un événement...'),
            'id': 'search-input'
        }),
        label=_('Recherche')
    )
    category = forms.ModelChoiceField(
        queryset=EventCategory.objects.filter(is_active=True).order_by('name'),
        required=False,
        empty_label=_("Toutes les catégories"),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=_('Catégorie')
    )
    location_city = forms.ChoiceField(
        choices=[('', _('Toutes les villes'))] + Location.ChadCityChoices.choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=_('Ville')
    )
    location_region = forms.ChoiceField(
        choices=[('', _('Toutes les régions'))] + Location.ChadRegionChoices.choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=_('Région')
    )
    event_type = forms.ChoiceField(
        choices=[('', _('Tous les types'))] + Event.EventTypeChoices.choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=_('Type d\'événement')
    )
    date_filter = forms.ChoiceField(
        choices=[
            ('', _('Toutes les dates')),
            ('upcoming', _('À venir')),
            ('ongoing', _('En cours')),
            ('today', _('Aujourd\'hui')),
            ('this_week', _('Cette semaine')),
            ('this_month', _('Ce mois')),
            ('past', _('Passés')),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=_('Période')
    )
    # Correction ici: Utiliser forms.ChoiceField avec des valeurs spécifiques
    is_online = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=_("Type de lieu"),
        choices=[
            ('', _('Tous les types de lieux')), # Value "" will be treated as None in get_queryset
            ('True', _('En ligne')),
            ('False', _('Physique')),
        ]
    )
    sort_by = forms.ChoiceField(
        choices=[
            ('start_date', _('Date de début (la plus proche en premier)')),
            ('-start_date', _('Date de début (la plus lointaine en premier)')),
            ('title', _('Titre (A-Z)')),
            ('-title', _('Titre (Z-A)')),
            ('category__name', _('Catégorie')),
            ('location__name', _('Lieu')),
        ],
        required=False,
        initial='start_date',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=_('Trier par')
    )