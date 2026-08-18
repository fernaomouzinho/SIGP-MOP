from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Insp, InspTracks

@receiver(post_save, sender=Insp)
def create_ver(sender, instance, created, **kwargs):
	if created:
		InspTracks.objects.create(id=instance.id, insp=instance)
