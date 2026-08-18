from django.urls import path
from .views import APICompanyList
urlpatterns = [
	# portal
	path('mobile/list/', APICompanyList.as_view(), name='api-company-list'),
]