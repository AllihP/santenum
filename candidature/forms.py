from django import forms
from django.core.exceptions import ValidationError
from .models import Candidature
import datetime

class CandidatureStep1Form(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ['nom', 'prenom', 'date_naissance', 'telephone', 'email', 'adresse', 'ville', 'code_postal']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre prénom'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+33123456789'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'votre.email@example.com'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Votre adresse complète'}),
            'ville': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre ville'}),
            'code_postal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '75000'}),
        }
    
    def clean_date_naissance(self):
        date_naissance = self.cleaned_data['date_naissance']
        age = (datetime.date.today() - date_naissance).days // 365
        if age < 18:
            raise ValidationError("Vous devez avoir au moins 18 ans.")
        return date_naissance

class CandidatureStep2Form(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ['niveau_etude', 'domaine_etude', 'etablissement', 'annee_diplome', 'experience_sante']
        widgets = {
            'niveau_etude': forms.Select(attrs={'class': 'form-control'}),
            'domaine_etude': forms.Select(attrs={'class': 'form-control'}),
            'etablissement': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de votre établissement'}),
            'annee_diplome': forms.NumberInput(attrs={'class': 'form-control', 'min': '1980', 'max': '2030'}),
            'experience_sante': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Décrivez votre expérience professionnelle dans le secteur de la santé...'}),
        }

class CandidatureStep3Form(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ['motivation', 'competences_techniques', 'disponibilite', 'salaire_souhaite']
        widgets = {
            'motivation': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Expliquez votre motivation à rejoindre notre équipe...'}),
            'competences_techniques': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Listez vos compétences techniques (langages, outils, certifications...)'}),
            'disponibilite': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Immédiate, dans 1 mois, etc.'}),
            'salaire_souhaite': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Montant en euros (optionnel)'}),
        }

class CandidatureStep4Form(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ['cv', 'lettre_motivation']
        widgets = {
            'cv': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'}),
            'lettre_motivation': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'}),
        }
    
    def clean_cv(self):
        cv = self.cleaned_data.get('cv')
        if cv:
            if cv.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError("Le fichier CV ne doit pas dépasser 5MB.")
        return cv



class CandidatureForm(forms.Form):
    nom = forms.CharField(max_length=100)
    prenom = forms.CharField(max_length=100)
    email = forms.EmailField()
    telephone = forms.CharField(max_length=15)
    poste = forms.CharField(max_length=200)
    cv = forms.FileField()
    lettre_motivation = forms.CharField(widget=forms.Textarea)