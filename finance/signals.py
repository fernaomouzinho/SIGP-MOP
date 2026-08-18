from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CPV, CPVReq, CPVReqTrack, CPVTrack, CPVLetter, PO, POTrack, POLetter, PRT, EV

@receiver(post_save, sender=CPVReq)
def create_cpvreq(sender, instance, created, **kwargs):
	if created:
		CPVReqTrack.objects.create(id=instance.id, cpvreq=instance)

@receiver(post_save, sender=CPV)
def create_cpv(sender, instance, created, **kwargs):
	if created:
		CPVTrack.objects.create(id=instance.id, cpv=instance)
		CPVLetter.objects.create(id=instance.id, cpv=instance, hashed=instance.hashed)

@receiver(post_save, sender=PO)
def create_po(sender, instance, created, **kwargs):
	if created:
		POTrack.objects.create(id=instance.id, po=instance)
		POLetter.objects.create(id=instance.id, po=instance, hashed=instance.hashed)

@receiver(post_save, sender=PRT)
def create_prt(sender, instance, created, **kwargs):
	if created:
		EV.objects.create(id=instance.id, prt=instance, cont=instance.cont, inv=instance.inv,\
			hashed=instance.hashed)
