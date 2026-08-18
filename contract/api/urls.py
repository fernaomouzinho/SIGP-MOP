from django.urls import path
from . import views
urlpatterns = [
	# portal
	path('portal/list/', views.APIPortalContList.as_view()),
	path('portal/hist/', views.APIPortalContHist.as_view()),
]