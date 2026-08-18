from django.urls import path
from .views import portal_auth_status

urlpatterns = [
	path("portal-auth-status/", portal_auth_status),
]