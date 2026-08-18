from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Project, ProjectLoc, ProjectEst

@receiver(post_save, sender=Project)
def create_project(sender, instance, created, **kwargs):
	if created:
		ProjectLoc.objects.create(id=instance.id, project=instance)
		ProjectEst.objects.create(id=instance.id, project=instance)