from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Employee, EmployeeDiv, EmployeePos

@receiver(post_save, sender=Employee)
def create_employee(sender, instance, created, **kwargs):
	if created:
		EmployeeDiv.objects.create(id=instance.id, employee=instance)
		EmployeePos.objects.create(id=instance.id, employee=instance)