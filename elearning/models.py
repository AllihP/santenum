# elearning/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
import uuid
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

# --- Modèle Utilisateur Personnalisé ---
class Utilisateur(AbstractUser):
    TYPE_UTILISATEUR_CHOICES = [
        ('expert_telemedecine', 'Expert en Télémédecine'),
        ('juriste', 'Juriste'),
        ('expert_informatique', 'Expert Informatique'),
        ('coach', 'Coach'),
        ('expert_biomedical', 'Expert Biomédical'),
        ('medecin', 'Médecin'),
        ('technicien', 'Technicien'),
        ('sage_femme', 'Sage-Femme'),
        ('paramedical', 'Paramédical'),
        ('pharmacien', 'Pharmacien'),
    ]
    type_utilisateur = models.CharField(
        max_length=50,
        choices=TYPE_UTILISATEUR_CHOICES,
        default='medecin',
        verbose_name="Type d'utilisateur"
    )
    telephone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Numéro de téléphone")
    profession_medicale = models.CharField(max_length=100, null=True, blank=True, verbose_name="Profession Médicale")
    niveau_acces = models.IntegerField(default=1, verbose_name="Niveau d'accès")

    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        null=True,
        blank=True,
        verbose_name="Photo de Profil"
    )

    # CHAMPS POUR RÉSOUDRE L'ERREUR fields.E336
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name="elearning_users_groups",
        related_query_name="elearning_user_group",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="elearning_users_permissions",
        related_query_name="elearning_user_permission",
    )

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.type_utilisateur})"

# --- Modèle Catégorie de Module ---
class CategorieModule(models.Model):
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom de la catégorie")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")

    class Meta:
        verbose_name = "Catégorie de Module"
        verbose_name_plural = "Catégories de Modules"
        ordering = ['nom']

    def __str__(self):
        return self.nom

# --- Modèle Module de Formation ---
class Module(models.Model):
    NIVEAU_CHOICES = [
        ('debutant', 'Débutant'),
        ('intermediaire', 'Intermédiaire'),
        ('avance', 'Avancé'),
    ]

    titre = models.CharField(max_length=255, verbose_name="Titre du module")
    description = models.TextField(null=True, blank=True, verbose_name="Description détaillée")
    niveau = models.CharField(
        max_length=20,
        choices=NIVEAU_CHOICES,
        default='debutant',
        verbose_name="Niveau du module"
    )
    categorie = models.ForeignKey(
        CategorieModule,
        on_delete=models.RESTRICT,
        related_name='modules',
        verbose_name="Catégorie"
    )
    requiert_certification = models.BooleanField(default=False, verbose_name="Requiert une certification")
    disponible_hors_ligne = models.BooleanField(default=True, verbose_name="Disponible hors ligne")
    createur = models.ForeignKey(
        'Utilisateur',
        on_delete=models.RESTRICT,
        related_name='modules_crees',
        verbose_name="Créateur du module"
    )
    image_module = models.ImageField(
        upload_to='module_covers/',
        null=True,
        blank=True,
        verbose_name="Image de couverture du module"
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de dernière modification")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Module de Formation"
        verbose_name_plural = "Modules de Formation"
        ordering = ['-date_creation']

    def __str__(self):
        return self.titre

# --- Modèle ModuleEnrollment pour l'inscription aux modules ---
class ModuleEnrollment(models.Model):
    user = models.ForeignKey(
        'Utilisateur',
        on_delete=models.CASCADE,
        related_name='module_enrollments',
        verbose_name="Utilisateur inscrit"
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name="Module de formation"
    )
    enrollment_date = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    completed = models.BooleanField(default=False, verbose_name="Complété")
    completion_date = models.DateTimeField(null=True, blank=True, verbose_name="Date de complétion")

    class Meta:
        unique_together = ('user', 'module')
        verbose_name = "Inscription au Module"
        verbose_name_plural = "Inscriptions aux Modules" # CORRIGÉ : était 'verbose_plural'

    def __str__(self):
        return f"{self.user.username} - {self.module.titre} ({'Terminé' if self.completed else 'En cours'})"


# --- NOUVEAUX MODÈLES POUR L'ÉVOLUTION ET L'ÉVALUATION ---

# 1. Modèle ContenuModule : Représente une unité de contenu dans un module (chapitre, vidéo, quiz, etc.)
class ContenuModule(models.Model):
    TYPE_CONTENU_CHOICES = [
        ('texte', 'Texte / Leçon'),
        ('video', 'Vidéo'),
        ('quiz', 'Quiz'),
        ('document', 'Document (PDF, Word, Image, etc.)'),
    ]

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='contenus',
        verbose_name="Module parent"
    )
    titre = models.CharField(max_length=255, verbose_name="Titre du contenu")
    type_contenu = models.CharField(max_length=20, choices=TYPE_CONTENU_CHOICES, verbose_name="Type de contenu")
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    description = models.TextField(null=True, blank=True, verbose_name="Description du contenu")

    contenu_textuel = models.TextField(null=True, blank=True, verbose_name="Contenu textuel (pour type 'texte')")
    url_video = models.URLField(max_length=500, null=True, blank=True, verbose_name="URL de la vidéo (pour type 'video')")
    fichier_document = models.FileField(
        upload_to='module_documents/',
        null=True,
        blank=True,
        verbose_name="Fichier du document (PDF, Word, Image, etc.)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contenu de Module"
        verbose_name_plural = "Contenus de Modules"
        ordering = ['module', 'ordre']
        unique_together = ('module', 'ordre')

    def __str__(self):
        return f"{self.module.titre} - {self.titre} ({self.get_type_contenu_display()})"


# 2. Modèle ProgressionContenu : Suivi de la progression d'un utilisateur dans un contenu spécifique
class ProgressionContenu(models.Model):
    user = models.ForeignKey(
        'Utilisateur',
        on_delete=models.CASCADE,
        related_name='progression_contenus',
        verbose_name="Utilisateur"
    )
    contenu_module = models.ForeignKey(
        ContenuModule,
        on_delete=models.CASCADE,
        related_name='progression_utilisateurs',
        verbose_name="Contenu du module"
    )
    completed = models.BooleanField(default=False, verbose_name="Complété")
    completion_date = models.DateTimeField(null=True, blank=True, verbose_name="Date de complétion")

    class Meta:
        verbose_name = "Progression du Contenu"
        verbose_name_plural = "Progression des Contenus"
        unique_together = ('user', 'contenu_module')

    def __str__(self):
        return f"{self.user.username} - {self.contenu_module.titre} ({'Terminé' if self.completed else 'En cours'})"

    def save(self, *args, **kwargs):
        if self.completed and not self.completion_date:
            self.completion_date = timezone.now()
        elif not self.completed:
            self.completion_date = None
        super().save(*args, **kwargs)

        total_contents = self.contenu_module.module.contenus.count()
        completed_contents = ProgressionContenu.objects.filter(
            user=self.user,
            contenu_module__module=self.contenu_module.module,
            completed=True
        ).count()

        if total_contents > 0 and total_contents == completed_contents:
            enrollment = ModuleEnrollment.objects.filter(
                user=self.user,
                module=self.contenu_module.module
            ).first()
            if enrollment and not enrollment.completed:
                enrollment.completed = True
                enrollment.completion_date = timezone.now()
                enrollment.save()


# 3. Modèle Quiz : Un quiz lié à un ContenuModule
class Quiz(models.Model):
    contenu_module = models.OneToOneField(
        ContenuModule,
        on_delete=models.CASCADE,
        related_name='quiz',
        verbose_name="Contenu de module (Quiz)"
    )
    titre = models.CharField(max_length=255, verbose_name="Titre du quiz")
    description = models.TextField(blank=True, verbose_name="Description du quiz")
    score_minimum = models.IntegerField(
        default=70,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Score minimum pour réussir (%)"
    )
    duree_limite_minutes = models.IntegerField(null=True, blank=True, verbose_name="Durée limite (minutes)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quiz" # CORRIGÉ : était 'verbose_plural'

    def __str__(self):
        return f"Quiz : {self.titre} (Module: {self.contenu_module.module.titre})"


# 4. Modèle Question : Une question de quiz
class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name="Quiz"
    )
    texte_question = models.TextField(verbose_name="Texte de la question")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions" # CORRIGÉ : était 'verbose_plural'
        ordering = ['id']

    def __str__(self):
        return f"Q: {self.texte_question[:50]}..."


# 5. Modèle ChoixReponse : Les options de réponse pour une question
class ChoixReponse(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choix',
        verbose_name="Question"
    )
    texte_choix = models.CharField(max_length=500, verbose_name="Texte du choix")
    est_correct = models.BooleanField(default=False, verbose_name="Est la bonne réponse")

    class Meta:
        verbose_name = "Choix de Réponse"
        verbose_name_plural = "Choix de Réponses" # CORRIGÉ : était 'verbose_plural'

    def __str__(self):
        return f"Choix pour '{self.question.texte_question[:30]}...': {self.texte_choix} ({'Correct' if self.est_correct else 'Faux'})"


# 6. Modèle ReponseUtilisateur : Enregistre la réponse d'un utilisateur à une question
class ReponseUtilisateur(models.Model):
    user = models.ForeignKey(
        'Utilisateur',
        on_delete=models.CASCADE,
        related_name='reponses_quiz',
        verbose_name="Utilisateur"
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='reponses_utilisateurs',
        verbose_name="Question"
    )
    choix_selectionne = models.ForeignKey(
        ChoixReponse,
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Choix sélectionné"
    )
    texte_reponse = models.TextField(null=True, blank=True, verbose_name="Réponse textuelle (si applicable)")
    date_reponse = models.DateTimeField(auto_now_add=True, verbose_name="Date de la réponse")
    est_correct = models.BooleanField(default=False, verbose_name="Est correcte")

    class Meta:
        verbose_name = "Réponse Utilisateur"
        verbose_name_plural = "Réponses Utilisateur" # CORRIGÉ : était 'verbose_plural'
        unique_together = ('user', 'question')

    def __str__(self):
        return f"{self.user.username} a répondu à {self.question.texte_question[:30]}..."

    def save(self, *args, **kwargs):
        if self.choix_selectionne:
            self.est_correct = self.choix_selectionne.est_correct
        else:
            self.est_correct = False
        super().save(*args, **kwargs)


# 7. Modèle ResultatQuiz : Stocke le score final d'un utilisateur pour un quiz
class ResultatQuiz(models.Model):
    user = models.ForeignKey(
        'Utilisateur',
        on_delete=models.CASCADE,
        related_name='resultats_quiz',
        verbose_name="Utilisateur"
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='resultats',
        verbose_name="Quiz"
    )
    score_obtenu = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Score obtenu (%)"
    )
    reussi = models.BooleanField(default=False, verbose_name="Réussi")
    date_tentative = models.DateTimeField(auto_now_add=True, verbose_name="Date de la tentative")

    class Meta:
        verbose_name = "Résultat de Quiz"
        verbose_name_plural = "Résultats de Quiz" # CORRIGÉ : était 'verbose_plural'
        ordering = ['-date_tentative']

    def __str__(self):
        return f"{self.user.username} - Quiz: {self.quiz.titre} - Score: {self.score_obtenu}% ({'Réussi' if self.reussi else 'Échoué'})"

    def save(self, *args, **kwargs):
        self.reussi = (self.score_obtenu >= self.quiz.score_minimum)
        super().save(*args, **kwargs)


# 8. Modèle Certificat : Pour les certifications (si requises par un Module)
class Certificat(models.Model):
    user = models.ForeignKey(
        'Utilisateur',
        on_delete=models.CASCADE,
        related_name='certificats',
        verbose_name="Utilisateur"
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='certificats_emis',
        verbose_name="Module certifié"
    )
    code_certification = models.CharField(max_length=100, unique=True, default=uuid.uuid4, verbose_name="Code de certification")
    date_emission = models.DateTimeField(auto_now_add=True, verbose_name="Date d'émission")

    class Meta:
        verbose_name = "Certificat"
        verbose_name_plural = "Certificats" # CORRIGÉ : était 'verbose_plural'
        unique_together = ('user', 'module')

    def __str__(self):
        return f"Certificat de {self.user.username} pour {self.module.titre}"