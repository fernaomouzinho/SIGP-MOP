from django.urls import path
from . import views

urlpatterns = [
    path('inv/list/', views.InspInvList, name="insp-inv-list"),
    #
    path('uvip/list/<str:hashid>/', views.uvipInspList, name="uvip-insp-list"),
    path('uvip/det/<str:hashid>/', views.uvipInspDet, name="uvip-insp-det"),
    path('uvip/add/<str:hashid>/', views.uvipInspAdd, name="uvip-insp-add"),
    path('uvip/edit/<str:hashid>/', views.uvipInspEdit, name="uvip-insp-edit"),
    path('uvip/rem/<str:pk>/', views.uvipInspRem, name="uvip-insp-rem"),
    path('uvip/send/<str:hashid>/', views.uvipInspSend, name="uvip-insp-send"),
    path('uvip/in/<str:hashid>/', views.uvipInspIn, name="uvip-insp-in"),
    path('uvip/com/edit/<str:hashid>/', views.uvipInspCommEdit, name="uvip-insp-com-edit"),
    path('uvip/end/<str:hashid>/', views.uvipInspEnd, name="uvip-insp-end"),
    #
    path('sec/list/', views.secInspList, name="sec-insp-list"),
    path('sec/det/<str:hashid>/', views.secInspDet, name="sec-insp-det"),
    path('sec/year/<str:year>/', views.secInspYear, name="sec-insp-year"),
    path('sec/back1/<str:hashid>/', views.secInspBack1, name="sec-insp-back1"),
    path('sec/in1/<str:hashid>/', views.secInspIn1, name="sec-insp-in1"),
    path('sec/add/<str:hashid>/', views.secInspAdd, name="sec-insp-add"),
    path('sec/edit/<str:hashid>/', views.secInspEdit, name="sec-insp-edit"),
    path('sec/rem/<str:pk>/', views.secInspRem, name="sec-insp-rem"),
    path('sec/send/<str:pk>/', views.secInspSend, name="sec-insp-send"),
    path('sec/in2/<str:hashid>/', views.secInspIn2, name="sec-insp-in2"),
    path('sec/com/edit/<str:hashid>/', views.secInspCommEdit, name="sec-insp-com-edit"),
    path('sec/end/<str:pk>/', views.secInspEnd, name="sec-insp-end"),
    path('sec/back/<str:pk>/', views.secInspBack, name="sec-insp-back"),
    # # eng
    path('eng/list/', views.engInspList, name="eng-insp-list"),
    path('eng/year/<str:year>/', views.engInspYear, name="eng-insp-year"),
    path('eng/det/<str:hashid>/', views.engInspDet, name="eng-insp-det"),
    path('eng/edit/<str:hashid>/', views.engInspEdit, name="eng-insp-edit"),
    path('eng/in/<str:hashid>/', views.engInspIn, name="eng-insp-in"),
    path('eng/send/<str:hashid>/', views.engInspSend, name="eng-insp-send"),
    # # All
    path('all/list/<str:hashid>/', views.allInspList, name="all-insp-list"),
    path('all/det/<str:hashid>/', views.allInspDet, name="all-insp-det"),
    ### PDF
    path('pdf/<str:pk>/', views.InspPDF, name="insp-pdf"),
    path('eng/pdf/<str:pk>/', views.InspSecPDF, name="insp-sec-pdf"),
    path('eng/pdf2/<str:pk>/', views.InspSecPDF2, name="insp-sec-pdf2"),
    path('eng/pdf3/<str:pk>/', views.InspSecPDF3, name="insp-sec-pdf3"),
]