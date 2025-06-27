from django.db import models
from django.core.validators import RegexValidator, FileExtensionValidator
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
import os




def validate_file_size(value):
    """Valide que le fichier ne dépasse pas 5MB"""
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5MB
        raise ValidationError("La taille du fichier ne peut pas dépasser 5MB.")


def cv_upload_path(instance, filename):
    """Génère un chemin personnalisé pour l'upload des CV"""
    ext = filename.split('.')[-1]
    # Utiliser l'email au lieu de l'ID qui peut ne pas exister encore
    safe_email = instance.email.replace('@', '_').replace('.', '_')
    filename = f"cv_{safe_email}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    return os.path.join('candidatures/cv/', filename)


def lettre_upload_path(instance, filename):
    """Génère un chemin personnalisé pour l'upload des lettres"""
    ext = filename.split('.')[-1]
    # Utiliser l'email au lieu de l'ID qui peut ne pas exister encore
    safe_email = instance.email.replace('@', '_').replace('.', '_')
    filename = f"lettre_{safe_email}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    return os.path.join('candidatures/lettres/', filename)


class Candidature(models.Model):
    NIVEAUX_ETUDE = [
        ('bac', 'Baccalauréat'),
        ('bac_plus_2', 'Bac+2 (BTS/DUT)'),
        ('licence', 'Licence (Bac+3)'),
        ('master', 'Master (Bac+5)'),
        ('doctorat', 'Doctorat'),
        ('autre', 'Autre'),
    ]
   
    DOMAINES_SANTE = [
        ('medecine', 'Médecine'),
        ('pharmacie', 'Pharmacie'),
        ('infirmier', 'Sciences Infirmières'),
        ('kinesitherapie', 'Kinésithérapie'),
        ('psychologie', 'Psychologie'),
        ('nutrition', 'Nutrition et Diététique'),
        ('informatique_sante', 'Informatique de Santé'),
        ('radiologie', 'Radiologie'),
        ('laboratoire', 'Analyses Médicales'),
        ('dentaire', 'Médecine Dentaire'),
        ('autre', 'Autre'),
    ]

    STATUTS_CANDIDATURE = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours d\'examen'),
        ('entretien', 'Convoqué(e) pour entretien'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
        ('retiree', 'Retirée par le candidat'),
    ]
   
    # Étape 1: Informations personnelles
    nom = models.CharField(
        max_length=100,
        help_text="Nom de famille"
    )
    prenom = models.CharField(
        max_length=100,
        help_text="Prénom(s)"
    )
    date_naissance = models.DateField(
        help_text="Format: JJ/MM/AAAA"
    )
    telephone = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            r'^\+?(?:[0-9] ?){6,14}[0-9]$',
            message="Format invalide. Ex: +33123456789 ou 0123456789"
        )],
        help_text="Numéro de téléphone avec indicatif pays si nécessaire"
    )
    email = models.EmailField(
        unique=True,
        help_text="Adresse email valide"
    )
    adresse = models.TextField(
        help_text="Adresse complète"
    )
    ville = models.CharField(max_length=100)
    code_postal = models.CharField(
        max_length=10,
        validators=[RegexValidator(
            r'^\d{5}$',
            message="Le code postal doit contenir 5 chiffres"
        )]
    )
   
    # Étape 2: Formation et expérience
    niveau_etude = models.CharField(
        max_length=20, 
        choices=NIVEAUX_ETUDE
    )
    domaine_etude = models.CharField(
        max_length=50, 
        choices=DOMAINES_SANTE
    )
    etablissement = models.CharField(
        max_length=200,
        help_text="Nom de l'établissement de formation"
    )
    annee_diplome = models.IntegerField(
        validators=[
            MinValueValidator(1950),
            MaxValueValidator(timezone.now().year + 5)
        ],
        help_text="Année d'obtention du diplôme"
    )
    experience_sante = models.TextField(
        help_text="Décrivez votre expérience dans le domaine de la santé (stages, emplois, bénévolat...)"
    )
    annees_experience = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(50)],
        help_text="Nombre d'années d'expérience professionnelle"
    )
   
    # Étape 3: Motivation et disponibilité
    motivation = models.TextField(
        help_text="Pourquoi souhaitez-vous rejoindre notre équipe? (500 mots maximum)"
    )
    competences_techniques = models.TextField(
        help_text="Décrivez vos compétences techniques et logiciels maîtrisés"
    )
    disponibilite = models.CharField(
        max_length=100,
        help_text="Immédiate, dans 1 mois, etc."
    )
    salaire_souhaite = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Salaire souhaité en euros (optionnel)"
    )
    temps_travail = models.CharField(
        max_length=50,
        choices=[
            ('temps_plein', 'Temps plein'),
            ('temps_partiel', 'Temps partiel'),
            ('stage', 'Stage'),
            ('freelance', 'Freelance/Consultant'),
        ],
        default='temps_plein'
    )
   
    # Étape 4: Documents
    cv = models.FileField(
        upload_to=cv_upload_path,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']),
            validate_file_size
        ],
        help_text="Format acceptés: PDF, DOC, DOCX (max 5MB)"
    )
    lettre_motivation = models.FileField(
        upload_to=lettre_upload_path,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']),
            validate_file_size
        ],
        help_text="Format acceptés: PDF, DOC, DOCX (max 5MB) - Optionnel"
    )
   
    # Métadonnées et suivi
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(
        default=False,
        help_text="Candidature complètement remplie"
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUTS_CANDIDATURE,
        default='en_attente'
    )
    notes_internes = models.TextField(
        blank=True,
        help_text="Notes internes pour l'équipe RH (non visible par le candidat)"
    )
    
    # Champs pour le suivi
    date_entretien = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="Date et heure de l'entretien programmé"
    )
    score_evaluation = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Score d'évaluation sur 100"
    )

    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Candidature"
        verbose_name_plural = "Candidatures"
        indexes = [
            models.Index(fields=['statut']),
            models.Index(fields=['domaine_etude']),
            models.Index(fields=['date_creation']),
        ]

    def clean(self):
        """Validation personnalisée"""
        super().clean()
        errors = {}
        
        # Vérifier que la date de naissance est cohérente
        if self.date_naissance and self.date_naissance > timezone.now().date():
            errors['date_naissance'] = "La date de naissance ne peut pas être dans le futur."
        
        # Vérifier l'âge minimum (16 ans pour un stage)
        if self.date_naissance:
            age = (timezone.now().date() - self.date_naissance).days // 365
            if age < 16:
                errors['date_naissance'] = "L'âge minimum requis est de 16 ans."
        
        # Vérifier la cohérence de l'année de diplôme
        if self.date_naissance and self.annee_diplome:
            age_diplome = self.annee_diplome - self.date_naissance.year
            if age_diplome < 16:
                errors['annee_diplome'] = "L'année de diplôme semble incohérente avec la date de naissance."
        
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        # Vérifier si la candidature est complète
        if (self.nom and self.prenom and self.email and self.telephone and 
            self.cv and self.motivation and self.competences_techniques):
            self.complete = True
        else:
            self.complete = False
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.get_domaine_etude_display()} ({self.get_statut_display()})"

    @property
    def age(self):
        """Calcule l'âge du candidat"""
        if self.date_naissance:
            return (timezone.now().date() - self.date_naissance).days // 365
        return None

    @property
    def nom_complet(self):
        """Retourne le nom complet"""
        return f"{self.prenom} {self.nom}"

    def peut_etre_contacte(self):
        """Détermine si le candidat peut être contacté pour un entretien"""
        return self.complete and self.statut in ['en_attente', 'en_cours']


# Modèle pour gérer les postes disponibles
class PosteDisponible(models.Model):
    TYPES_CONTRAT = [
        ('cdi', 'CDI'),
        ('cdd', 'CDD'),
        ('stage', 'Stage'),
        ('freelance', 'Freelance'),
        ('interim', 'Intérim'),
    ]

    titre = models.CharField(max_length=200)
    description = models.TextField()
    domaines_requis = models.CharField(
        max_length=50,
        choices=Candidature.DOMAINES_SANTE
    )
    niveau_requis = models.CharField(
        max_length=20,
        choices=Candidature.NIVEAUX_ETUDE
    )
    type_contrat = models.CharField(
        max_length=20,
        choices=TYPES_CONTRAT
    )
   
    localisation = models.CharField(max_length=200)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_limite = models.DateField(null=True, blank=True)
    actif = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Poste Disponible"
        verbose_name_plural = "Postes Disponibles"

    def __str__(self):
        return f"{self.titre} - {self.localisation}"


# Modèle pour lier candidatures et postes
class CandidaturePoste(models.Model):
    candidature = models.ForeignKey(
        Candidature,
        on_delete=models.CASCADE,
        related_name='postes_candidats'
    )
    poste = models.ForeignKey(
        PosteDisponible,
        on_delete=models.CASCADE,
        related_name='candidatures'
    )
    date_candidature = models.DateTimeField(auto_now_add=True)
    priorite = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Priorité du candidat pour ce poste (1 = plus haute)"
    )

    class Meta:
        unique_together = ['candidature', 'poste']
        ordering = ['priorite', '-date_candidature']

    def __str__(self):
        return f"{self.candidature.nom_complet} -> {self.poste.titre}"
    


