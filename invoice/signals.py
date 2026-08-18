from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Invoice, InvTrack
from finance.models import PRT

@receiver(post_save, sender=Invoice)
def create_invoice(sender, instance, created, **kwargs):
	if created:
		InvTrack.objects.create(id=instance.id, inv=instance)
