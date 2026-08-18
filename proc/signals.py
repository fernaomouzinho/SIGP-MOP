from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Proc, ProcReqTrack, ProcResTrack, ProcTrack

@receiver(post_save, sender=Proc)
def create_proc(sender, instance, created, **kwargs):
	if created:
		ProcReqTrack.objects.create(id=instance.id, proc=instance)
		ProcResTrack.objects.create(id=instance.id, proc=instance)
		ProcTrack.objects.create(id=instance.id, proc=instance)