from django.urls import path
from . import views
urlpatterns = [
	path('list/', views.APIProjList.as_view()),
	path('<str:year>/', views.APIProjYears.as_view()),
    # portal
	path('portal/home/', views.APIPortalHome.as_view()),
	path('portal/mopcat/', views.APIPPortalMOpCat.as_view()),
	path('portal/cat/', views.APIPPortalProjCat.as_view()),
	path('portal/cap/', views.APIPPortalProjCap.as_view()),
	path('portal/sec/', views.APIPPortalProjSec.as_view()),
]