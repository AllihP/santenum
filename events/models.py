# events/models.py

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.validators import FileExtensionValidator, MinLengthValidator, EmailValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

# Utiliser get_user_model pour la compatibilité avec un modèle User personnalisé
User = get_user_model()


class EventCategory(models.Model):
    """
    Modèle pour définir les catégories d'événements de santé numérique.
    Ces catégories sont prédéfinies et aident à classer les événements.
    """

    class CategoryChoices(models.TextChoices):
        """Choix prédéfinis pour les catégories d'événements."""
        TELEMEDICINE = 'TELEMEDICINE', _('Télémédecine')
        BIOTECHNOLOGY = 'BIOTECHNOLOGY', _('Biotechnologie')
        DATA_ANALYSIS = 'DATA_ANALYSIS', _('Analyse de données')
        MOBILE_HEALTH = 'MOBILE_HEALTH', _('Santé mobile (mHealth)')
        AI_HEALTH = 'AI_HEALTH', _('Intelligence artificielle en santé')
        ELECTRONIC_HEALTH_RECORDS = 'ELECTRONIC_HEALTH_RECORDS', _('Dossiers médicaux électroniques')
        DIGITAL_THERAPEUTICS = 'DIGITAL_THERAPEUTICS', _('Thérapeutiques numériques')
        HEALTH_EDUCATION = 'HEALTH_EDUCATION', _('Éducation à la santé numérique')
        E_PRESCRIPTION = 'E_PRESCRIPTION', _('E-prescription')
        BIG_DATA = 'BIG_DATA', _('Big Data en santé')
        CYBERSECURITY = 'CYBERSECURITY', _('Cybersécurité en santé')
        ROBOTICS = 'ROBOTICS', _('Robotique médicale')
        OTHER = 'OTHER', _('Autre')

    name = models.CharField(_("Nom de la catégorie"), max_length=100, unique=True,
                            choices=CategoryChoices.choices,
                            default=CategoryChoices.TELEMEDICINE)
    description = models.TextField(_("Description"), blank=True, null=True)
    is_active = models.BooleanField(_("Actif"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Catégorie d'événement")
        verbose_name_plural = _("Catégories d'événements")
        ordering = ['name']

    def __str__(self):
        return self.get_name_display()


class Location(models.Model):
    """
    Modèle pour représenter les lieux d'événements.
    """

    class ChadCityChoices(models.TextChoices):
        """Choix des grandes villes du Tchad."""
        NDJAMENA = 'NDJAMENA', _('N\'Djamena')
        ABECHE = 'ABECHE', _('Abéché')
        MOUNDOU = 'MOUNDOU', _('Moundou')
        SARH = 'SARH', _('Sarh')
        KUMRA = 'KUMRA', _('Koumra')
        PALA = 'PALA', _('Pala')
        AMTIMAN = 'AMTIMAN', _('Am Timan')
        DOBA = 'DOBA', _('Doba')
        BONGOR = 'BONGOR', _('Bongor')
        FADA = 'FADA', _('Fada')
        OTHER = 'OTHER', _('Autre')

    class ChadRegionChoices(models.TextChoices):
        """Choix des régions du Tchad."""
        CHAD = 'CHAD', _('Tchad (Général)') # Pour les événements qui ne sont pas liés à une région spécifique
        NDJAMENA = 'NDJAMENA', _('N\'Djamena')
        CHARI_BAGUIRMI = 'CHARI_BAGUIRMI', _('Chari-Baguirmi')
        HADJER_LAMIS = 'HADJER_LAMIS', _('Hadjer-Lamis')
        KANEM = 'KANEM', _('Kanem')
        LAC = 'LAC', _('Lac')
        BATHA = 'BATHA', _('Batha')
        BORKOU = 'BORKOU', _('Borkou')
        ENNEDI_EST = 'ENNEDI_EST', _('Ennedi Est')
        ENNEDI_OUEST = 'ENNEDI_OUEST', _('Ennedi Ouest')
        GUERA = 'GUERA', _('Guéra')
        TANDJILE = 'TANDJILE', _('Tandjilé')
        MANDJOUL = 'MANDJOUL', _('Mandoul')
        MAYOKEB_EST = 'MAYOKEB_EST', _('Mayo-Kebbi Est')
        MAYOKEB_OUEST = 'MAYOKEB_OUEST', _('Mayo-Kebbi Ouest')
        MOYEN_CHARI = 'MOYEN_CHARI', _('Moyen-Chari')
        OUADDAI = 'OUADDAI', _('Ouaddaï')
        SALAMAT = 'SALAMAT', _('Salamat')
        SILA = 'SILA', _('Sila')
        TIBESTI = 'TIBESTI', _('Tibesti')
        WADI_FIRA = 'WADI_FIRA', _('Wadi Fira')
        LOGONE_OCCIDENTAL = 'LOGONE_OCCIDENTAL', _('Logone Occidental')
        LOGONE_ORIENTAL = 'LOGONE_ORIENTAL', _('Logone Oriental')
        OTHER = 'OTHER', _('Autre Région')


    name = models.CharField(_("Nom du lieu"), max_length=200, help_text=_("Nom de l'établissement, salle, etc."))
    address = models.CharField(_("Adresse"), max_length=255, blank=True, null=True)
    city = models.CharField(_("Ville"), max_length=100, blank=True, null=True,
                            choices=ChadCityChoices.choices, default=ChadCityChoices.NDJAMENA)
    region = models.CharField(_("Région"), max_length=100, blank=True, null=True,
                              choices=ChadRegionChoices.choices, default=ChadRegionChoices.NDJAMENA)
    latitude = models.DecimalField(_("Latitude"), max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(_("Longitude"), max_digits=9, decimal_places=6, blank=True, null=True)
    capacity = models.PositiveIntegerField(_("Capacité d'accueil"), blank=True, null=True)
    has_electricity = models.BooleanField(_("Dispose d'électricité"), default=False)
    has_internet = models.BooleanField(_("Dispose d'internet"), default=False)
    accessibility = models.TextField(_("Informations sur l'accessibilité"), blank=True, null=True)
    contact_person = models.CharField(_("Personne contact"), max_length=100, blank=True, null=True)
    contact_phone = models.CharField(_("Téléphone contact"), max_length=20, blank=True, null=True)
    is_active = models.BooleanField(_("Actif"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Lieu")
        verbose_name_plural = _("Lieux")
        unique_together = ('name', 'city', 'region') # Pour éviter les doublons exacts
        ordering = ['name']

    def __str__(self):
        parts = [self.name]
        if self.city and self.city != self.ChadCityChoices.OTHER:
            parts.append(self.get_city_display())
        elif self.address:
            parts.append(self.address)
        return ", ".join(parts)


class Partner(models.Model):
    """
    Modèle pour représenter les partenaires d'événements.
    """

    class PartnerTypeChoices(models.TextChoices):
        ORGANIZATION = 'ORGANIZATION', _('Organisation')
        COMPANY = 'COMPANY', _('Entreprise')
        INDIVIDUAL = 'INDIVIDUAL', _('Individu')
        GOVERNMENT = 'GOVERNMENT', _('Gouvernement / Institution Publique')
        NGO = 'NGO', _('ONG')
        ACADEMIC = 'ACADEMIC', _('Institution Académique')
        MEDIA = 'MEDIA', _('Média')
        OTHER = 'OTHER', _('Autre')

    class PartnershipTypeChoices(models.TextChoices):
        SPONSOR = 'SPONSOR', _('Sponsor')
        MEDIA_PARTNER = 'MEDIA_PARTNER', _('Partenaire Média')
        COLLABORATOR = 'COLLABORATOR', _('Collaborateur')
        HOST = 'HOST', _('Hôte du lieu')
        SUPPORTER = 'SUPPORTER', _('Partenaire de soutien')
        OTHER = 'OTHER', _('Autre')

    name = models.CharField(_("Nom du partenaire"), max_length=200, unique=True)
    description = models.TextField(_("Description"), blank=True, null=True)
    type = models.CharField(_("Type de partenaire"), max_length=50,
                            choices=PartnerTypeChoices.choices, default=PartnerTypeChoices.ORGANIZATION)
    partnership_type = models.CharField(_("Type de partenariat"), max_length=50,
                                        choices=PartnershipTypeChoices.choices, default=PartnershipTypeChoices.SPONSOR)
    logo = models.ImageField(_("Logo"), upload_to='partners_logos/', blank=True, null=True,
                             validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif', 'svg'])])
    website = models.URLField(_("Site web"), max_length=200, blank=True, null=True)
    contact_person = models.CharField(_("Personne contact"), max_length=100, blank=True, null=True)
    contact_email = models.EmailField(_("Email contact"), blank=True, null=True, validators=[EmailValidator()])
    contact_phone = models.CharField(_("Téléphone contact"), max_length=20, blank=True, null=True)
    license_number = models.CharField(_("Numéro de licence (Tchad)"), max_length=50, blank=True, null=True,
                                      help_text=_("Numéro d'agrément ou d'autorisation pour les entités au Tchad"))
    tax_id = models.CharField(_("Numéro d'identification fiscale (Tchad)"), max_length=50, blank=True, null=True,
                              help_text=_("NIF ou autre identifiant fiscal au Tchad"))
    is_active = models.BooleanField(_("Actif"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Partenaire")
        verbose_name_plural = _("Partenaires")
        ordering = ['name']

    def __str__(self):
        return self.name


class Event(models.Model):
    """
    Modèle pour les événements de santé numérique.
    """

    class EventTypeChoices(models.TextChoices):
        """Choix du type d'événement (conférence, atelier, etc.)."""
        CONFERENCE = 'CONFERENCE', _('Conférence')
        WORKSHOP = 'WORKSHOP', _('Atelier')
        SEMINAR = 'SEMINAR', _('Séminaire')
        WEBINAR = 'WEBINAR', _('Webinaire')
        HACKATHON = 'HACKATHON', _('Hackathon')
        TRAINING = 'TRAINING', _('Formation')
        MEETING = 'MEETING', _('Réunion')
        EXPO = 'EXPO', _('Exposition / Salon')
        OTHER = 'OTHER', _('Autre')

    class EventStatusChoices(models.TextChoices):
        """Statut de publication de l'événement."""
        DRAFT = 'DRAFT', _('Brouillon')
        PENDING_REVIEW = 'PENDING_REVIEW', _('En attente de validation')
        PUBLISHED = 'PUBLISHED', _('Publié')
        ARCHIVED = 'ARCHIVED', _('Archivé')
        CANCELLED = 'CANCELLED', _('Annulé')
        COMPLETED = 'COMPLETED', _('Terminé')

    title = models.CharField(_("Titre de l'événement"), max_length=255, unique=True,
                             validators=[MinLengthValidator(5)])
    slug = models.SlugField(_("Slug"), max_length=255, unique=True, blank=True)
    description = models.TextField(_("Description complète de l'événement"))
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True,
                                 related_name='events', verbose_name=_("Catégorie"))
    type = models.CharField(_("Type d'événement"), max_length=50,
                            choices=EventTypeChoices.choices, default=EventTypeChoices.CONFERENCE)
    status = models.CharField(_("Statut de l'événement"), max_length=50,
                              choices=EventStatusChoices.choices, default=EventStatusChoices.DRAFT)

    start_date = models.DateTimeField(_("Date et heure de début"))
    end_date = models.DateTimeField(_("Date et heure de fin"))
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='events', verbose_name=_("Lieu physique"))
    is_online = models.BooleanField(_("Est en ligne"), default=False,
                                    help_text=_("Cochez si l'événement est entièrement en ligne."))
    online_url = models.URLField(_("Lien de l'événement en ligne"), max_length=500, blank=True, null=True)
    registration_deadline = models.DateTimeField(_("Date limite d'inscription"), null=True, blank=True)
    
    max_participants = models.PositiveIntegerField(_("Nombre max de participants"), null=True, blank=True,
                                                   validators=[MinValueValidator(1)],
                                                   help_text=_("Laisser vide pour un nombre illimité."))
    current_participants = models.PositiveIntegerField(_("Participants actuels"), default=0) # Ajout pour suivi
    target_audience = models.TextField(_("Public cible"), blank=True, null=True,
                                       help_text=_("Décrivez qui devrait assister à cet événement."))
    program = models.TextField(_("Programme / Agenda"), blank=True, null=True)

    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='organized_events', verbose_name=_("Organisateur"))
    contact_email = models.EmailField(_("Email de contact de l'événement"), blank=True, null=True,
                                      validators=[EmailValidator()])
    contact_phone = models.CharField(_("Téléphone de contact de l'événement"), max_length=20, blank=True, null=True)

    partners = models.ManyToManyField(Partner, blank=True, verbose_name=_("Partenaires de l'événement"))

    published_at = models.DateTimeField(_("Date de publication"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Événement")
        verbose_name_plural = _("Événements")
        ordering = ['start_date']

    def __str__(self):
        return self.title

    def clean(self):
        """
        Validations personnalisées pour l'événement.
        """
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            raise ValidationError(_("La date de début doit être antérieure à la date de fin."))

        if self.registration_deadline:
            if self.registration_deadline >= self.start_date:
                raise ValidationError(_("La date limite d'inscription doit être antérieure à la date de début de l'événement."))

        if self.is_online and not self.online_url:
            raise ValidationError(_("Un événement en ligne doit avoir un lien en ligne (URL)."))
        
        if not self.is_online and not self.location:
             raise ValidationError(_("Un événement physique doit avoir un lieu physique."))

        # Assurer que max_participants est None ou >= current_participants
        if self.max_participants is not None and self.current_participants > self.max_participants:
            raise ValidationError(_("Le nombre actuel de participants ne peut pas dépasser le nombre maximum de participants."))


    def save(self, *args, **kwargs):
        """
        Surcharge la méthode save pour générer le slug et gérer la date de publication.
        """
        if not self.slug:
            self.slug = slugify(self.title)

        # Gérer la date de publication
        if self.status == self.EventStatusChoices.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        elif self.status != self.EventStatusChoices.PUBLISHED and self.published_at:
            self.published_at = None # Réinitialiser si le statut change de 'PUBLISHED'

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Retourne l'URL canonique pour un événement."""
        return reverse('events:event_detail', kwargs={'slug': self.slug})

    @property
    def is_upcoming(self):
        """Vérifie si l'événement est à venir."""
        return self.end_date and self.end_date >= timezone.now() and self.status == self.EventStatusChoices.PUBLISHED

    @property
    def is_ongoing(self):
        """Vérifie si l'événement est en cours."""
        now = timezone.now()
        return self.start_date <= now <= self.end_date and self.status == self.EventStatusChoices.PUBLISHED

    @property
    def is_past(self):
        """Vérifie si l'événement est passé."""
        return self.end_date and self.end_date < timezone.now() and self.status == self.EventStatusChoices.PUBLISHED

    @property
    def is_registration_open(self):
        """Vérifie si les inscriptions sont ouvertes."""
        if self.registration_deadline:
            return timezone.now() < self.registration_deadline and self.status == self.EventStatusChoices.PUBLISHED
        # Si pas de date limite, les inscriptions sont ouvertes tant que l'événement n'est pas passé
        return not self.is_past and self.status == self.EventStatusChoices.PUBLISHED

    @property
    def available_slots(self):
        """Calcule les places disponibles."""
        if self.max_participants is None:
            return None # Nombre illimité
        return max(0, self.max_participants - self.current_participants)

    @property
    def has_available_slots(self):
        """Vérifie s'il reste des places."""
        if self.max_participants is None:
            return True # Nombre illimité
        return self.current_participants < self.max_participants


class EventRegistration(models.Model):
    """
    Modèle pour enregistrer les participants aux événements.
    """

    class RegistrationStatusChoices(models.TextChoices):
        PENDING = 'PENDING', _('En attente')
        CONFIRMED = 'CONFIRMED', _('Confirmé')
        CANCELLED = 'CANCELLED', _('Annulé')
        ATTENDED = 'ATTENDED', _('A participé')
        NO_SHOW = 'NO_SHOW', _('Non présenté')

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations',
                              verbose_name=_("Événement"))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='event_registrations', verbose_name=_("Utilisateur (si connecté)"))
    # Informations de l'inscrit si non connecté ou complémentaires
    first_name = models.CharField(_("Prénom"), max_length=100)
    last_name = models.CharField(_("Nom"), max_length=100)
    email = models.EmailField(_("Email"), validators=[EmailValidator()])
    phone_number = models.CharField(_("Numéro de téléphone"), max_length=20, blank=True, null=True)
    
    registration_date = models.DateTimeField(_("Date d'inscription"), auto_now_add=True)
    status = models.CharField(_("Statut d'inscription"), max_length=50,
                              choices=RegistrationStatusChoices.choices, default=RegistrationStatusChoices.PENDING)
    
    confirmed_at = models.DateTimeField(_("Date de confirmation"), null=True, blank=True)
    cancelled_at = models.DateTimeField(_("Date d'annulation"), null=True, blank=True)
    
    # Champ pour des notes ou demandes spéciales
    notes = models.TextField(_("Notes / Demandes spéciales"), blank=True, null=True)

    class Meta:
        verbose_name = _("Inscription à l'événement")
        verbose_name_plural = _("Inscriptions aux événements")
        unique_together = ('event', 'email') # Un seul enregistrement par email et événement
        ordering = ['registration_date']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.event.title}"

    def clean(self):
        """
        Validations personnalisées pour l'inscription.
        """
        # S'assurer qu'un utilisateur connecté ou des infos personnelles sont fournis
        if not self.user and (not self.first_name or not self.last_name or not self.email):
            raise ValidationError(_("Pour les inscriptions sans utilisateur connecté, le prénom, le nom et l'email sont requis."))

        # Vérifier si l'événement est éligible pour l'inscription
        if not self.event.is_registration_open:
            raise ValidationError(
                {'event': _("Les inscriptions pour cet événement sont fermées ou l'événement n'est pas publié.")}
            )
        
        # Vérifier les places disponibles (si l'événement a une limite)
        if self.event.max_participants is not None:
            # On ne compte que les inscriptions qui ne sont ni annulées ni des non-présentations
            active_registrations_count = self.event.registrations.exclude(
                status__in=[
                    self.RegistrationStatusChoices.CANCELLED,
                    self.RegistrationStatusChoices.NO_SHOW
                ]
            ).count()

            # Si c'est une nouvelle inscription ou un changement de statut vers "actif"
            if self.pk is None or self.status in [self.RegistrationStatusChoices.PENDING, self.RegistrationStatusChoices.CONFIRMED]:
                # On ne prend pas en compte l'inscription actuelle si elle existe déjà et est valide
                if self.pk and self.status == self.RegistrationStatusChoices.CONFIRMED:
                    pass # Déjà compté si c'est un update qui ne change pas le statut
                elif active_registrations_count >= self.event.max_participants:
                    raise ValidationError(
                        {'event': _("Désolé, toutes les places pour cet événement sont déjà prises.")}
                    )


    def save(self, *args, **kwargs):
        """
        Surcharge la méthode save pour gérer les dates de confirmation/annulation
        et mettre à jour le compteur de participants de l'événement.
        """
        # Gérer la date de confirmation/annulation selon le statut
        if self.status == self.RegistrationStatusChoices.CONFIRMED and not self.confirmed_at:
            self.confirmed_at = timezone.now()
            self.cancelled_at = None  # S'assurer que l'annulation est réinitialisée si re-confirmée
        elif self.status == self.RegistrationStatusChoices.CANCELLED and not self.cancelled_at:
            self.cancelled_at = timezone.now()
            self.confirmed_at = None  # S'assurer que la confirmation est réinitialisée si annulée
        elif self.status not in [self.RegistrationStatusChoices.CONFIRMED, self.RegistrationStatusChoices.CANCELLED]:
            self.confirmed_at = None
            self.cancelled_at = None

        super().save(*args, **kwargs)
        
        # Mettre à jour le compteur current_participants de l'événement
        # On ne compte que les inscriptions actives (PENDING, CONFIRMED, ATTENDED)
        self.event.current_participants = self.event.registrations.filter(
            status__in=[
                self.RegistrationStatusChoices.PENDING,
                self.RegistrationStatusChoices.CONFIRMED,
                self.RegistrationStatusChoices.ATTENDED
            ]
        ).count()
        self.event.save(update_fields=['current_participants']) # Éviter une boucle infinie de save


    def delete(self, *args, **kwargs):
        """
        Surcharge la méthode delete pour décrémenter le compteur de participants
        lorsqu'une inscription est supprimée.
        """
        event = self.event # Sauvegarder l'événement avant la suppression de l'inscription
        super().delete(*args, **kwargs)
        # Recalculer et mettre à jour le compteur après suppression
        event.current_participants = event.registrations.filter(
            status__in=[
                self.RegistrationStatusChoices.PENDING,
                self.RegistrationStatusChoices.CONFIRMED,
                self.RegistrationStatusChoices.ATTENDED
            ]
        ).count()
        event.save(update_fields=['current_participants'])


    @property
    def full_name(self):
        """Retourne le nom complet du participant."""
        return f"{self.first_name} {self.last_name}"

    @property
    def can_be_cancelled(self):
        """
        Indique si l'inscription peut être annulée.
        Une inscription peut être annulée si elle est confirmée et que l'événement est à venir.
        """
        return (self.status == self.RegistrationStatusChoices.CONFIRMED or self.status == self.RegistrationStatusChoices.PENDING) and self.event.is_upcoming