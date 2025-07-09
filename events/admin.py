# events/admin.py

from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import Event, EventRegistration, EventCategory, Location, Partner


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'status', 'category', 'location', 'organizer', 'is_online', 'current_participants', 'published_at')
    list_filter = ('status', 'category', 'location__city', 'is_online')
    search_fields = ('title', 'description', 'target_audience')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_date'
    filter_horizontal = ('partners',)
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'category', 'type', 'status')
        }),
        (_('Dates et lieu'), {
            'fields': ('start_date', 'end_date', 'location', 'is_online', 'online_url', 'registration_deadline')
        }),
        (_('Participants et programme'), {
            'fields': ('max_participants', 'current_participants', 'target_audience', 'program')
        }),
        (_('Organisation et contact'), {
            'fields': ('organizer', 'contact_email', 'contact_phone', 'partners', 'published_at')
        }),
    )
    readonly_fields = ('current_participants', 'published_at', 'created_at', 'updated_at') # current_participants est géré par le système


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'event', 'email', 'status', 'registration_date', 'confirmed_at', 'cancelled_at')
    list_filter = ('status', 'event__category', 'event__location__city', 'registration_date')
    search_fields = ('first_name', 'last_name', 'email', 'event__title')
    date_hierarchy = 'registration_date'
    actions = ['cancel_registrations', 'confirm_registrations']
    readonly_fields = ('registration_date', 'confirmed_at', 'cancelled_at') # Dates gérées automatiquement

    fieldsets = (
        (None, {
            'fields': ('event', 'user', 'first_name', 'last_name', 'email', 'phone_number', 'status', 'notes')
        }),
        (_('Dates de statut'), {
            'fields': ('registration_date', 'confirmed_at', 'cancelled_at'),
            'classes': ('collapse',),
        }),
    )

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = _("Nom complet")

    @admin.action(description=_('Annuler les inscriptions sélectionnées'))
    def cancel_registrations(self, request, queryset):
        updated_count = queryset.filter(status__in=[
            EventRegistration.RegistrationStatusChoices.PENDING,
            EventRegistration.RegistrationStatusChoices.CONFIRMED
        ]).update(
            status=EventRegistration.RegistrationStatusChoices.CANCELLED,
            cancelled_at=timezone.now(),
            confirmed_at=None # Assurer que la date de confirmation est effacée si on annule
        )
        self.message_user(request, _(f"{updated_count} inscriptions ont été annulées avec succès."), level='success')

    @admin.action(description=_('Confirmer les inscriptions sélectionnées'))
    def confirm_registrations(self, request, queryset):
        updated_count = queryset.filter(status=EventRegistration.RegistrationStatusChoices.PENDING).update(
            status=EventRegistration.RegistrationStatusChoices.CONFIRMED,
            confirmed_at=timezone.now(),
            cancelled_at=None # Assurer que la date d'annulation est effacée si on confirme
        )
        self.message_user(request, _(f"{updated_count} inscriptions ont été confirmées avec succès."), level='success')


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'region', 'capacity', 'is_active', 'contact_person', 'contact_phone')
    list_filter = ('is_active', 'city', 'region', 'has_electricity', 'has_internet')
    search_fields = ('name', 'address', 'contact_person', 'contact_phone')
    fieldsets = (
        (None, {
            'fields': ('name', 'address', 'city', 'region')
        }),
        (_('Informations supplémentaires'), {
            'fields': ('latitude', 'longitude', 'capacity', 'has_electricity', 'has_internet', 'accessibility'),
            'classes': ('collapse',),
        }),
        (_('Contact'), {
            'fields': ('contact_person', 'contact_phone', 'is_active'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'partnership_type', 'is_active', 'website')
    list_filter = ('is_active', 'type', 'partnership_type')
    search_fields = ('name', 'description', 'contact_person', 'contact_email')
    fieldsets = (
        (None, {
            'fields': ('name', 'type', 'partnership_type', 'logo', 'website', 'is_active')
        }),
        (_('Contact et détails'), {
            'fields': ('contact_email', 'contact_person', 'contact_phone', 'description'),
            'classes': ('collapse',),
        }),
        (_('Informations spécifiques au Tchad'), {
            'fields': ('license_number', 'tax_id'),
            'classes': ('collapse',),
        }),
    )

