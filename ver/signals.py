from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Ver, VerTracks

@receiver(post_save, sender=Ver)
def create_ver(sender, instance, created, **kwargs):
	if created:
		VerTracks.objects.create(id=instance.id, ver=instance)
