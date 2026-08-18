from django.urls import path
from . import views
urlpatterns = [
	
    path('list/', views.APIInvoiceList.as_view(), name='invoice-list'),
    path('tracking/', views.APIInvoiceTracking.as_view(), name='invoice-tracking'),
	
]