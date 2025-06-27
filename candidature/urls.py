from django.urls import path
from . import views

app_name = 'candidature'

urlpatterns = [
    path('candidature/', views.candidature, name='candidature'),
]