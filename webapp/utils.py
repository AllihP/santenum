import os
from django.conf import settings
from django.core.files.storage import default_storage

def handle_uploaded_file(uploaded_file, subfolder='candidatures'):
    """Gère l'upload sécurisé des fichiers"""
    # Vérifications de sécurité
    allowed_extensions = ['.pdf', '.doc', '.docx']
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise ValueError("Type de fichier non autorisé")
    
    if uploaded_file.size > 5 * 1024 * 1024:  # 5MB
        raise ValueError("Fichier trop volumineux")
    
    return uploaded_file

def send_candidature_notification(candidature):
    """Fonction utilitaire pour l'envoi d'emails"""
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import render_to_string
    
    try:
        subject = f"Nouvelle candidature - {candidature.prenom} {candidature.nom}"
        
        context = {'candidature': candidature}
        html_content = render_to_string('candidature/email_candidature.html', context)
        text_content = render_to_string('candidature/email_candidature.txt', context)
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CANDIDATURE_EMAIL],
            reply_to=[candidature.email]
        )
        
        email.attach_alternative(html_content, "text/html")
        
        # Joindre les fichiers
        if candidature.cv:
            email.attach_file(candidature.cv.path)
        if candidature.lettre_motivation:
            email.attach_file(candidature.lettre_motivation.path)
        
        return email.send()
    
    except Exception as e:
        # Log l'erreur
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Erreur envoi email candidature {candidature.id}: {str(e)}")
        return False
