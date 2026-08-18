from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.CompanyList, name="comp-list"),
    path('add/', views.CompanyAdd, name="comp-add"),
    path('edit/<str:hashid>/', views.CompanyEdit, name="comp-edit"),
    path('detail/<str:hashid>/', views.CompanyDetail, name="comp-det"),
    path('u/det/', views.uCompDet, name="comp-u-det"),
    #
    path('u/create/<str:pk>/', views.CompUserCreate, name="comp-user-create"),
    path('u/reset/<str:pk>/', views.CompPassReset, name="comp-user-reset"),
    path('u/ena/<str:pk>/', views.CompPassEna, name="comp-user-ena"),
    path('u/dis/<str:pk>/', views.CompPassDis, name="comp-user-dis"),
   
]