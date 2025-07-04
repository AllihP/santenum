# Generated by Django 5.2.1 on 2025-06-24 14:09

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('TELEMEDICINE', 'Télémédecine'), ('BIOTECHNOLOGY', 'Biotechnologie'), ('DATA_ANALYSIS', 'Analyse de données'), ('MOBILE_HEALTH', 'Santé mobile (mHealth)'), ('AI_HEALTH', 'Intelligence artificielle en santé'), ('ELECTRONIC_HEALTH_RECORDS', 'Dossiers médicaux électroniques'), ('DIGITAL_THERAPEUTICS', 'Thérapeutiques numériques'), ('HEALTH_EDUCATION', 'Éducation à la santé numérique'), ('E_PRESCRIPTION', 'E-prescription'), ('BIG_DATA', 'Big Data en santé'), ('CYBERSECURITY', 'Cybersécurité en santé'), ('ROBOTICS', 'Robotique médicale'), ('OTHER', 'Autre')], default='TELEMEDICINE', max_length=100, unique=True, verbose_name='Nom de la catégorie')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Actif')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': "Catégorie d'événement",
                'verbose_name_plural': "Catégories d'événements",
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Nom du partenaire')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('type', models.CharField(choices=[('ORGANIZATION', 'Organisation'), ('COMPANY', 'Entreprise'), ('INDIVIDUAL', 'Individu'), ('GOVERNMENT', 'Gouvernement / Institution Publique'), ('NGO', 'ONG'), ('ACADEMIC', 'Institution Académique'), ('MEDIA', 'Média'), ('OTHER', 'Autre')], default='ORGANIZATION', max_length=50, verbose_name='Type de partenaire')),
                ('partnership_type', models.CharField(choices=[('SPONSOR', 'Sponsor'), ('MEDIA_PARTNER', 'Partenaire Média'), ('COLLABORATOR', 'Collaborateur'), ('HOST', 'Hôte du lieu'), ('SUPPORTER', 'Partenaire de soutien'), ('OTHER', 'Autre')], default='SPONSOR', max_length=50, verbose_name='Type de partenariat')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='partners_logos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif', 'svg'])], verbose_name='Logo')),
                ('website', models.URLField(blank=True, null=True, verbose_name='Site web')),
                ('contact_person', models.CharField(blank=True, max_length=100, null=True, verbose_name='Personne contact')),
                ('contact_email', models.EmailField(blank=True, max_length=254, null=True, validators=[django.core.validators.EmailValidator()], verbose_name='Email contact')),
                ('contact_phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Téléphone contact')),
                ('license_number', models.CharField(blank=True, help_text="Numéro d'agrément ou d'autorisation pour les entités au Tchad", max_length=50, null=True, verbose_name='Numéro de licence (Tchad)')),
                ('tax_id', models.CharField(blank=True, help_text='NIF ou autre identifiant fiscal au Tchad', max_length=50, null=True, verbose_name="Numéro d'identification fiscale (Tchad)")),
                ('is_active', models.BooleanField(default=True, verbose_name='Actif')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Partenaire',
                'verbose_name_plural': 'Partenaires',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Nom de l'établissement, salle, etc.", max_length=200, verbose_name='Nom du lieu')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Adresse')),
                ('city', models.CharField(blank=True, choices=[('NDJAMENA', "N'Djamena"), ('ABECHE', 'Abéché'), ('MOUNDOU', 'Moundou'), ('SARH', 'Sarh'), ('KUMRA', 'Koumra'), ('PALA', 'Pala'), ('AMTIMAN', 'Am Timan'), ('DOBA', 'Doba'), ('BONGOR', 'Bongor'), ('FADA', 'Fada'), ('OTHER', 'Autre')], default='NDJAMENA', max_length=100, null=True, verbose_name='Ville')),
                ('region', models.CharField(blank=True, choices=[('CHAD', 'Tchad (Général)'), ('NDJAMENA', "N'Djamena"), ('CHARI_BAGUIRMI', 'Chari-Baguirmi'), ('HADJER_LAMIS', 'Hadjer-Lamis'), ('KANEM', 'Kanem'), ('LAC', 'Lac'), ('BATHA', 'Batha'), ('BORKOU', 'Borkou'), ('ENNEDI_EST', 'Ennedi Est'), ('ENNEDI_OUEST', 'Ennedi Ouest'), ('GUERA', 'Guéra'), ('TANDJILE', 'Tandjilé'), ('MANDJOUL', 'Mandoul'), ('MAYOKEB_EST', 'Mayo-Kebbi Est'), ('MAYOKEB_OUEST', 'Mayo-Kebbi Ouest'), ('MOYEN_CHARI', 'Moyen-Chari'), ('OUADDAI', 'Ouaddaï'), ('SALAMAT', 'Salamat'), ('SILA', 'Sila'), ('TIBESTI', 'Tibesti'), ('WADI_FIRA', 'Wadi Fira'), ('LOGONE_OCCIDENTAL', 'Logone Occidental'), ('LOGONE_ORIENTAL', 'Logone Oriental'), ('OTHER', 'Autre Région')], default='NDJAMENA', max_length=100, null=True, verbose_name='Région')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Latitude')),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Longitude')),
                ('capacity', models.PositiveIntegerField(blank=True, null=True, verbose_name="Capacité d'accueil")),
                ('has_electricity', models.BooleanField(default=False, verbose_name="Dispose d'électricité")),
                ('has_internet', models.BooleanField(default=False, verbose_name="Dispose d'internet")),
                ('accessibility', models.TextField(blank=True, null=True, verbose_name="Informations sur l'accessibilité")),
                ('contact_person', models.CharField(blank=True, max_length=100, null=True, verbose_name='Personne contact')),
                ('contact_phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Téléphone contact')),
                ('is_active', models.BooleanField(default=True, verbose_name='Actif')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Lieu',
                'verbose_name_plural': 'Lieux',
                'ordering': ['name'],
                'unique_together': {('name', 'city', 'region')},
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, validators=[django.core.validators.MinLengthValidator(5)], verbose_name="Titre de l'événement")),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='Slug')),
                ('description', models.TextField(verbose_name="Description complète de l'événement")),
                ('type', models.CharField(choices=[('CONFERENCE', 'Conférence'), ('WORKSHOP', 'Atelier'), ('SEMINAR', 'Séminaire'), ('WEBINAR', 'Webinaire'), ('HACKATHON', 'Hackathon'), ('TRAINING', 'Formation'), ('MEETING', 'Réunion'), ('EXPO', 'Exposition / Salon'), ('OTHER', 'Autre')], default='CONFERENCE', max_length=50, verbose_name="Type d'événement")),
                ('status', models.CharField(choices=[('DRAFT', 'Brouillon'), ('PENDING_REVIEW', 'En attente de validation'), ('PUBLISHED', 'Publié'), ('ARCHIVED', 'Archivé'), ('CANCELLED', 'Annulé'), ('COMPLETED', 'Terminé')], default='DRAFT', max_length=50, verbose_name="Statut de l'événement")),
                ('start_date', models.DateTimeField(verbose_name='Date et heure de début')),
                ('end_date', models.DateTimeField(verbose_name='Date et heure de fin')),
                ('is_online', models.BooleanField(default=False, help_text="Cochez si l'événement est entièrement en ligne.", verbose_name='Est en ligne')),
                ('online_url', models.URLField(blank=True, max_length=500, null=True, verbose_name="Lien de l'événement en ligne")),
                ('registration_deadline', models.DateTimeField(blank=True, null=True, verbose_name="Date limite d'inscription")),
                ('max_participants', models.PositiveIntegerField(blank=True, help_text='Laisser vide pour un nombre illimité.', null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Nombre max de participants')),
                ('current_participants', models.PositiveIntegerField(default=0, verbose_name='Participants actuels')),
                ('target_audience', models.TextField(blank=True, help_text='Décrivez qui devrait assister à cet événement.', null=True, verbose_name='Public cible')),
                ('program', models.TextField(blank=True, null=True, verbose_name='Programme / Agenda')),
                ('contact_email', models.EmailField(blank=True, max_length=254, null=True, validators=[django.core.validators.EmailValidator()], verbose_name="Email de contact de l'événement")),
                ('contact_phone', models.CharField(blank=True, max_length=20, null=True, verbose_name="Téléphone de contact de l'événement")),
                ('published_at', models.DateTimeField(blank=True, null=True, verbose_name='Date de publication')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('organizer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organized_events', to=settings.AUTH_USER_MODEL, verbose_name='Organisateur')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='events.eventcategory', verbose_name='Catégorie')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='events.location', verbose_name='Lieu physique')),
                ('partners', models.ManyToManyField(blank=True, to='events.partner', verbose_name="Partenaires de l'événement")),
            ],
            options={
                'verbose_name': 'Événement',
                'verbose_name_plural': 'Événements',
                'ordering': ['start_date'],
            },
        ),
        migrations.CreateModel(
            name='EventRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='Prénom')),
                ('last_name', models.CharField(max_length=100, verbose_name='Nom')),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()], verbose_name='Email')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Numéro de téléphone')),
                ('registration_date', models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")),
                ('status', models.CharField(choices=[('PENDING', 'En attente'), ('CONFIRMED', 'Confirmé'), ('CANCELLED', 'Annulé'), ('ATTENDED', 'A participé'), ('NO_SHOW', 'Non présenté')], default='PENDING', max_length=50, verbose_name="Statut d'inscription")),
                ('confirmed_at', models.DateTimeField(blank=True, null=True, verbose_name='Date de confirmation')),
                ('cancelled_at', models.DateTimeField(blank=True, null=True, verbose_name="Date d'annulation")),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes / Demandes spéciales')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='events.event', verbose_name='Événement')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_registrations', to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur (si connecté)')),
            ],
            options={
                'verbose_name': "Inscription à l'événement",
                'verbose_name_plural': 'Inscriptions aux événements',
                'ordering': ['registration_date'],
                'unique_together': {('event', 'email')},
            },
        ),
    ]
