
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, 
    DeleteView, TemplateView, FormView
)
from django.views import View
from django.http import JsonResponse, HttpResponse, Http404
from django.db.models import Q, Count, Avg, Prefetch
from django.utils import timezone
from django.core.paginator import Paginator
from django.urls import reverse_lazy, reverse
import json







from django.shortcuts import render , redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.utils import translation
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout



from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .models import Candidature
import os
from django.utils.translation import gettext_lazy as _
from .forms import CandidatureForm
import logging

logger = logging.getLogger(__name__)
# views.py
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Candidature
from .forms import CandidatureStep1Form, CandidatureStep2Form, CandidatureStep3Form, CandidatureStep4Form


def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if email:
            # Logique pour sauvegarder l'email (base de données, service externe, etc.)
            # Exemple : NewsletterSubscription.objects.create(email=email)
            
            messages.success(request, 'Inscription réussie à la newsletter!')
            return redirect('success_page')  # ou retourner JsonResponse pour AJAX
        else:
            messages.error(request, 'Veuillez fournir une adresse email valide.')
    
    return render(request, 'newsletter_form.html')



def candidature_step1(request):
    if request.method == 'POST':
        form = CandidatureStep1Form(request.POST)
        if form.is_valid():
            candidature = form.save(commit=False)
            candidature.save()
            request.session['candidature_id'] = candidature.id
            messages.success(request, 'Étape 1 complétée avec succès!')
            return redirect('candidature_step2')
    else:
        form = CandidatureStep1Form()
    
    return render(request, 'candidature/step1.html', {
        'form': form,
        'step': 1,
        'total_steps': 4
    })

def candidature_step2(request):
    candidature_id = request.session.get('candidature_id')
    if not candidature_id:
        messages.error(request, 'Veuillez commencer par l\'étape 1.')
        return redirect('candidature_step1')
    
    candidature = get_object_or_404(Candidature, id=candidature_id)
    
    if request.method == 'POST':
        form = CandidatureStep2Form(request.POST, instance=candidature)
        if form.is_valid():
            form.save()
            messages.success(request, 'Étape 2 complétée avec succès!')
            return redirect('candidature_step3')
    else:
        form = CandidatureStep2Form(instance=candidature)
    
    return render(request, 'candidature/step2.html', {
        'form': form,
        'candidature': candidature,
        'step': 2,
        'total_steps': 4
    })

def candidature_step3(request):
    candidature_id = request.session.get('candidature_id')
    if not candidature_id:
        messages.error(request, 'Veuillez commencer par l\'étape 1.')
        return redirect('candidature_step1')
    
    candidature = get_object_or_404(Candidature, id=candidature_id)
    
    if request.method == 'POST':
        form = CandidatureStep3Form(request.POST, instance=candidature)
        if form.is_valid():
            form.save()
            messages.success(request, 'Étape 3 complétée avec succès!')
            return redirect('candidature_step4')
    else:
        form = CandidatureStep3Form(instance=candidature)
    
    return render(request, 'candidature/step3.html', {
        'form': form,
        'candidature': candidature,
        'step': 3,
        'total_steps': 4
    })

def candidature_step4(request):
    candidature_id = request.session.get('candidature_id')
    if not candidature_id:
        messages.error(request, 'Veuillez commencer par l\'étape 1.')
        return redirect('candidature_step1')
    
    candidature = get_object_or_404(Candidature, id=candidature_id)
    
    if request.method == 'POST':
        form = CandidatureStep4Form(request.POST, request.FILES, instance=candidature)
        if form.is_valid():
            candidature = form.save(commit=False)
            candidature.complete = True
            candidature.save()
            
            # Envoyer l'email
            send_candidature_email(candidature)
            
            messages.success(request, 'Candidature soumise avec succès! Vous recevrez une réponse sous 48h.')
            del request.session['candidature_id']
            return redirect('candidature_success')
    else:
        form = CandidatureStep4Form(instance=candidature)
    
    return render(request, 'candidature/step4.html', {
        'form': form,
        'candidature': candidature,
        'step': 4,
        'total_steps': 4
    })

def send_candidature_email(candidature):
    """Envoie un email avec les détails de la candidature"""
    subject = f"Nouvelle candidature - {candidature.prenom} {candidature.nom}"
    
    # Contexte pour le template email
    context = {
        'candidature': candidature,
    }
    
    # Rendu du template HTML
    html_content = render_to_string('candidature/email_candidature.html', context)
    text_content = render_to_string('candidature/email_candidature.txt', context)
    
    # Création de l'email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.CANDIDATURE_EMAIL],  # Votre email
        reply_to=[candidature.email]
    )
    
    # Ajout du contenu HTML
    email.attach_alternative(html_content, "text/html")
    
    # Ajout des fichiers
    if candidature.cv:
        email.attach_file(candidature.cv.path)
    if candidature.lettre_motivation:
        email.attach_file(candidature.lettre_motivation.path)
    
    # Envoi
    email.send()

def candidature_success(request):
    return render(request, 'candidature/success.html')

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('candidature/etape-1/', views.candidature_step1, name='candidature_step1'),
    path('candidature/etape-2/', views.candidature_step2, name='candidature_step2'),
    path('candidature/etape-3/', views.candidature_step3, name='candidature_step3'),
    path('candidature/etape-4/', views.candidature_step4, name='candidature_step4'),
    path('candidature/succes/', views.candidature_success, name='candidature_success'),
    path('evenements/newsletter', views.candidature_success, name='newsletter_subscribe'),
]



def index(request):
    return render(request, './app/index.html', {})

def base(request):
    return render(request, './app/base.html', {})

def footer(request):
    return render(request, './app/footer.html', {})

def navbar(request):
    return render(request, './app/navbar.html', {})

def preloader(request):
    return render(request, './app/preloader.html', {})

def step1(request):
    return render(request, './app/step1.html', {})

def step2(request):
    return render(request, './app/step2.html', {})

def step3(request):
    return render(request, './app/step3.html', {})

def step4(request):
    return render(request, './app/step4.html', {})

def services(request):
    return render(request, 'app/services.html', {})

def soins(request):
    return render(request, 'app/soins.html', {})

def technologies(request):
    return render(request, 'app/technologies.html', {})

def candidatureForm(request):
    return render(request, 'app/candidatureForm.html', {})

def evenements(request):
    return render(request, './app/evenements.html', {})

def formations(request):
    return render(request, './app/formation.html', {})

def applications(request):
    return render(request, './app/applications.html', {})

def technologie(request):
    return render(request, './app/technologie.html', {})

def suivi(request):
    return render(request, './app/suivi.html', {})

def suggestions(request):
    return render(request, './app/suggestions.html', {})

def soins(request):
    return render(request, './app/soins.html', {})

def lab(request):
    return render(request, './app/lab.html', {})

def immersion(request):
    return render(request, './app/immersion.html', {})

def consulter(request):
    return render(request, './app/consulter.html', {})

def administration(request):
    return render(request, './app/administration.html', {})

def candidature(request):
    return render(request, './app/candidature.html', {})

def suggestion(request):
    return render(request, './app/suggestion.html', {})

def language_selector(request):
    return render(request, './app/language_selector.html', {})



def soins_view(request):
    return render(request, 'services/soins.html', {'title': 'Service de l’offre de soins'})



def index(request):
    """Vue pour la page d'accueil avec support multilingue"""
    context = {
        'page_title': _('À propos'),
        'current_language': translation.get_language(),
    }
    return render(request, './app/index.html', context)

def services(request):
    """Vue pour la page des services"""
    context = {
        'page_title': _('Nos Services'),
        'current_language': translation.get_language(),
    }
    return render(request, './app/services.html', context)

def santenumerique(request):
    """Vue pour la page des applications"""
    context = {
        'page_title': _('Applications'),
        'current_language': translation.get_language(),
    }
    return render(request, './app/santenumerique.html', context)

def formations(request):
    """Vue pour la page des formations"""
    context = {
        'page_title': _('Formations'),
        'current_language': translation.get_language(),
    }
    return render(request, './app/formations.html', context)

def evenements(request):
    """Vue pour la page des événements"""
    context = {
        'page_title': _('Événements'),
        'current_language': translation.get_language(),
    }
    return render(request, './app/evenements.html', context)

def candidature(request):
    """Vue pour la page des candidatures"""
    context = {
        'page_title': _('Candidatures'),
        'current_language': translation.get_language(),
    }
    return render(request, './app/candidature.html', context)

def candidatureForm(request):
    """Vue pour la page des candidatures"""
    context = {
        'page_title': _('CandidatureForm'),
        'current_language': translation.get_language(),
    }
    return render(request, './app/candidature.html', context)



def suggestion(request):
    """Vue pour la page des suggestions"""
    context = {
        'page_title': _('Suggestions'),
        'current_language': translation.get_language(),
    }
    return render(request, './app/suggestion.html', context)




