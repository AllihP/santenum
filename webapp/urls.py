from django.urls import path
from . import views

app_name = 'webapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('administration/', views.administration, name='administration'),
    path('consulter/', views.consulter, name='consulter'),
    path('evenements/', views.evenements, name='evenements'),
    path('formations/', views.formations, name='formations'),
    path('immersion/', views.immersion, name='immersion'),
    path('lab/', views.lab, name='lab'),
    path('apllications/', views.applications, name='applications'),
    path('soins/', views.soins, name='soins'),
    path('technologies/', views.soins, name='technologies'),
    path('suivi/', views.suivi, name='suivi'),
    path('suggestions/', views.suggestions, name='suggestions'),
    path('technologie/', views.technologie, name='technologie'),
    path('candidature/', views.candidature, name='candidature'),
    path('suggestion/', views.suggestion, name='suggestion'),
    path('base/', views.base, name='base'),
    path('step1/', views.base, name='step1'),
    path('step2/', views.base, name='step2'),
    path('step3/', views.base, name='step3'),
    path('step4/', views.base, name='step4'),

    path('candidatureForm/', views.base, name='candidatureForm'),
    
]



