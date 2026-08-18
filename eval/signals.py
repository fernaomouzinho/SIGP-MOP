from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Eval, EvalTrack, EvalFITrack

@receiver(post_save, sender=Eval)
def create_eval(sender, instance, created, **kwargs):
	if created:
		category = instance.proj.pcategory.code 
		if category == "LM":
			EvalTrack.objects.create(id=instance.id, eval=instance)
		else:
			EvalFITrack.objects.create(id=instance.id, eval=instance)