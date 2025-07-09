
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
# urls.py
from django.urls import path
from . import views

@login_required
def profile_view(request):
    # This is a placeholder for a generic project-level profile view
    return render(request, 'accounts/profile.html', {'user': request.user})

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




