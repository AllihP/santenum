# management/commands/cleanup_incomplete_candidatures.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from myapp.models import Candidature

class Command(BaseCommand):
    help = 'Supprime les candidatures incomplètes de plus de 7 jours'
    
    def handle(self, *args, **options):
        cutoff_date = timezone.now() - timedelta(days=7)
        
        candidatures_to_delete = Candidature.objects.filter(
            complete=False,
            date_creation__lt=cutoff_date
        )
        
        count = candidatures_to_delete.count()
        candidatures_to_delete.delete()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Supprimé {count} candidature(s) incomplète(s)'
            )
        )

# signals.py (optionnel - pour notifications)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Candidature

@receiver(post_save, sender=Candidature)
def candidature_complete_notification(sender, instance, created, **kwargs):
    """Envoie une notification quand une candidature est complétée"""
    if not created and instance.complete:
        # Email de confirmation au candidat
        send_mail(
            subject='Candidature reçue - Confirmation',
            message=f"""
Bonjour {instance.prenom} {instance.nom},

Nous avons bien reçu votre candidature pour rejoindre notre équipe de santé numérique.

Notre équipe RH l'examinera dans les plus brefs délais et vous contactera dans les 48 heures.

Cordialement,
L'équipe RH
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=True,
        )