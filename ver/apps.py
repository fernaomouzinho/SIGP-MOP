from django.apps import AppConfig


class VerConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'ver'
	
	def ready(self):
		import ver.signals
