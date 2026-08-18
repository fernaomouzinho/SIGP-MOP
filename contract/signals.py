from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Contract, Amendment, ContPay

@receiver(post_save, sender=Contract)
def create_contract(sender, instance, created, **kwargs):
	if created:
		Amendment.objects.create(id=instance.id, contract=instance, hashed=instance.hashed)
		# ContPay.objects.create(id=instance.id, contract=instance)
