# elearning/forms.py
from django import forms
from .models import Module, Utilisateur

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['titre', 'description', 'niveau', 'categorie', 'requiert_certification', 'disponible_hors_ligne']
        # Tu pourrais exclure 'createur', 'date_creation', 'date_modification' car auto-gérés ou définis à la création

class InscriptionUtilisateurForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Utilisateur
        fields = ['username', 'first_name', 'last_name', 'email', 'type_utilisateur', 'telephone', 'profession_medicale']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError(
                "Les mots de passe ne correspondent pas."
            )
        return cleaned_data