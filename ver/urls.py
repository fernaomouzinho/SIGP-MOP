from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.VerList, name="ver-list"),
    #
    path('uvip/list/<str:hashid>/', views.uvipVerList, name="uvip-ver-list"),
    path('uvip/det/<str:hashid>/', views.uvipVerDet, name="uvip-ver-det"),
    path('uvip/add/<str:hashid>/', views.uvipVerAdd, name="uvip-ver-add"),
    path('uvip/edit/<str:hashid>/', views.uvipVerEdit, name="uvip-ver-edit"),
    path('uvip/rem/<str:pk>/', views.uvipVerRem, name="uvip-ver-rem"),
    path('uvip/send/<str:hashid>/', views.uvipVerSend, name="uvip-ver-send"),
    path('uvip/in/<str:hashid>/', views.uvipVerIn, name="uvip-ver-in"),
    path('uvip/com/edit/<str:hashid>/', views.uvipVerCommEdit, name="uvip-ver-com-edit"),
    path('uvip/end/<str:hashid>/', views.uvipVerEnd, name="uvip-ver-end"),
    #
    path('sec/list/', views.secVerList, name="sec-ver-list"),
    path('sec/det/<str:hashid>/', views.secVerDet, name="sec-ver-det"),
    path('sec/year/<str:year>/', views.secVerYear, name="sec-ver-year"),
    path('sec/back1/<str:hashid>/', views.secVerBack1, name="sec-ver-back1"),
    path('sec/in1/<str:hashid>/', views.secVerIn1, name="sec-ver-in1"),
    path('sec/add/<str:hashid>/', views.secVerAdd, name="sec-ver-add"),
    path('sec/edit/<str:hashid>/', views.secVerEdit, name="sec-ver-edit"),
    path('sec/rem/<str:pk>/', views.secVerRem, name="sec-ver-rem"),
    path('sec/send/<str:pk>/', views.secVerSend, name="sec-ver-send"),
    path('sec/in2/<str:hashid>/', views.secVerIn2, name="sec-ver-in2"),
    path('sec/com/edit/<str:hashid>/', views.secVerCommEdit, name="sec-ver-com-edit"),
    path('sec/end/<str:pk>/', views.secVerEnd, name="sec-ver-end"),
    path('sec/back/<str:pk>/', views.secVerBack, name="sec-ver-back"),
    # # eng
    path('eng/list/', views.engVerList, name="eng-ver-list"),
    path('eng/year/<str:year>/', views.engVerYear, name="eng-ver-year"),
    path('eng/det/<str:hashid>/', views.engVerDet, name="eng-ver-det"),
    path('eng/edit/<str:hashid>/', views.engVerEdit, name="eng-ver-edit"),
    path('eng/in/<str:hashid>/', views.engVerIn, name="eng-ver-in"),
    path('eng/send/<str:hashid>/', views.engVerSend, name="eng-ver-send"),
    # # All
    path('all/list/<str:hashid>/', views.allVerList, name="all-ver-list"),
    path('all/det/<str:hashid>/', views.allVerDet, name="all-ver-det"),
    ### PDF
    path('pdf/<str:pk>/', views.VerPDF, name="ver-pdf"),
    path('eng/pdf/<str:pk>/', views.VerSecPDF, name="ver-sec-pdf"),
    path('eng/pdf2/<str:pk>/', views.VerSecPDF2, name="ver-sec-pdf2"),
    path('eng/pdf3/<str:pk>/', views.VerSecPDF3, name="ver-sec-pdf3"),
]