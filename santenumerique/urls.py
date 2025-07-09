from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

# Les URL non localisées (comme l'admin)
urlpatterns = [
    path('admin/', admin.site.urls),  # L'URL d'administration est maintenant ici, hors de i18n_patterns
    path('i18n/', include('django.conf.urls.i18n')), # Pour la gestion des langues de Django
    # Ajoutez ici d'autres URLs qui ne doivent PAS être localisées
]

# Les URL qui seront préfixées par le code de langue (ex: /en/ma-page, /fr/ma-page)
urlpatterns += i18n_patterns(
    path('', include('webapp.urls')),
    path('', include('events.urls')),
    # Si newsletter.urls est une application distincte et ne se chevauche pas avec events.urls
    path('newsletter/', include('events.urls')), # Vérifiez si cela n'est pas redondant avec 'events.urls'
    path('', include('candidature.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # URLs d'authentification supplémentaires (vérifiez si 'accounts/' ci-dessous ne les rend pas redondantes)
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    path('accounts/', include('django.contrib.auth.urls')), # Inclut les vues par défaut de Django (connexion/déconnexion/reset password)
                                                          # Attention: si vous avez listé des vues d'auth ci-dessus manuellement,
                                                          # cela peut créer des duplicatas. Gardez soit l'include, soit les vues individuelles.
    path('', include('elearning.urls')),
    path('elearning/', include('elearning.urls')), # Vérifiez si cela n'est pas redondant avec le path vide précédent

    # L'argument prefix_default_language=False DOIT être le dernier argument de i18n_patterns
    prefix_default_language=False
)

# Servir les fichiers statiques et média UNIQUEMENT en mode développement (DEBUG=True)
# En production, Nginx les sert directement, donc ce bloc est ignoré.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)