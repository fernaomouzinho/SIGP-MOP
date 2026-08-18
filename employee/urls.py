from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.EmpList, name="emp-list"),
    path('add/', views.EmpAdd, name="emp-add"),
    path('edit/<str:hashid>/', views.EmpEdit, name="emp-edit"),
    path('detail/<str:hashid>/', views.EmpDetail, name="emp-det"),
    #
    path('div/edit/<str:hashid>/<str:pk>/', views.EmpDivEdit, name="emp-div-edit"),
    path('div/rem/<str:hashid>/<str:pk>/', views.EmpDivRem, name="emp-div-rem"),
    path('pos/edit/<str:hashid>/<str:pk>/', views.EmpPosEdit, name="emp-pos-edit"),
    path('pos/rem/<str:hashid>/<str:pk>/', views.EmpPosRem, name="emp-pos-rem"),
   
]