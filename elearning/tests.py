from django.test import TestCase
from django.urls import reverse
from .models import CategorieModule, Module, Utilisateur
from django.contrib.auth import get_user_model

class ModuleModelTest(TestCase):
    def test_module_creation(self):
        # Crée un utilisateur pour le module
        user = get_user_model().objects.create_user(username='testuser', password='password123', email='test@example.com', type_utilisateur='medecin')
        # Crée une catégorie
        category = CategorieModule.objects.create(nom='Test Catégorie')
        # Crée un module
        module = Module.objects.create(
            titre='Module de Test',
            description='Ceci est un module de test.',
            niveau='debutant',
            categorie=category,
            createur=user
        )
        self.assertEqual(module.titre, 'Module de Test')
        self.assertEqual(module.categorie.nom, 'Test Catégorie')
        self.assertEqual(module.createur.username, 'testuser')

class ModuleViewsTest(TestCase):
    def setUp(self):
        # Crée un utilisateur de test connecté pour les vues protégées
        self.user = get_user_model().objects.create_user(username='testviewer', password='password123', email='viewer@example.com', type_utilisateur='medecin')
        self.client.login(username='testviewer', password='password123')

        # Crée des données pour les tests de vues
        self.category = CategorieModule.objects.create(nom='Test Catégorie Vue')
        self.module = Module.objects.create(
            titre='Module Vue Test',
            description='Description du module de test de vue.',
            niveau='debutant',
            categorie=self.category,
            createur=self.user
        )

    def test_liste_modules_view(self):
        response = self.client.get(reverse('elearning:liste_modules'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Module Vue Test')
        self.assertTemplateUsed(response, 'elearning/liste_modules.html')

    def test_detail_module_view(self):
        response = self.client.get(reverse('elearning:detail_module', args=[self.module.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Module Vue Test')
        self.assertTemplateUsed(response, 'elearning/detail_module.html')