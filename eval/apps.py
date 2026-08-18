from django.apps import AppConfig


class EvalConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'eval'

	def ready(self):
		import eval.signals
