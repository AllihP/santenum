from django.urls import path
from . import views

app_name = 'elearning'

urlpatterns = [
    path('', views.home_page, name='home'), # <<< AJOUTE CETTE LIGNE
    path('modules/', views.liste_modules, name='liste_modules'),
    path('modules/<int:module_id>/', views.detail_module, name='detail_module'),
    path('dashboard/', views.tableau_de_bord, name='tableau_de_bord'),
    path('profile/', views.mon_profil, name='mon_profil'), 
]
