from django.test import TestCase

# tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.sessions.models import Session
from .models import Candidature
from .forms import CandidatureStep1Form, CandidatureStep2Form
import datetime

class CandidatureFormTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_step1_form_valid(self):
        """Test du formulaire étape 1 avec données valides"""
        form_data = {
            'nom': 'Dupont',
            'prenom': 'Jean',
            'date_naissance': '1990-05-15',
            'telephone': '+33123456789',
            'email': 'jean.dupont@email.com',
            'adresse': '123 Rue de la Santé',
            'ville': 'Paris',
            'code_postal': '75001'
        }
        form = CandidatureStep1Form(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_step1_age_validation(self):
        """Test de validation de l'âge minimum"""
        form_data = {
            'nom': 'Jeune',
            'prenom': 'Trop',
            'date_naissance': '2010-01-01',  # Trop jeune
            'telephone': '+33123456789',
            'email': 'trop.jeune@email.com',
            'adresse': '123 Rue',
            'ville': 'Paris',
            'code_postal': '75001'
        }
        form = CandidatureStep1Form(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date_naissance', form.errors)
    
    def test_complete_workflow(self):
        """Test du workflow complet"""
        # Étape 1
        response = self.client.post(reverse('candidature_step1'), {
            'nom': 'Test',
            'prenom': 'User',
            'date_naissance': '1990-01-01',
            'telephone': '+33123456789',
            'email': 'test@example.com',
            'adresse': '123 Test Street',
            'ville': 'Test City',
            'code_postal': '12345'
        })
        self.assertEqual(response.status_code, 302)
        
        # Vérifier que la candidature a été créée
        candidature = Candidature.objects.filter(email='test@example.com').first()
        self.assertIsNotNone(candidature)
        self.assertFalse(candidature.complete)
