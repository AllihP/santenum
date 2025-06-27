# events/urls.py
from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    # Exemple d'URL pour le détail d'un événement (à décommenter si EventDetailView existe)
    # path('<slug:slug>/', views.EventDetailView.as_view(), name='event_detail'),
]