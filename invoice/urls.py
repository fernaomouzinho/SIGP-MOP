from django.urls import path
from . import views

urlpatterns = [
   # sup
    path('sup/cont/list/', views.supInvContList, name="sup-inv-cont-list"),
    path('sup/list/<str:hashid>/', views.supInvList, name="sup-inv-list"),
    path('sup/add/<str:hashid>/', views.supInvAdd, name="sup-inv-add"),
    path('sup/det/<str:hashid>/', views.supInvDet, name="sup-inv-det"),
    path('sup/edit/<str:hashid>/<str:hashid2>/', views.supInvEdit, name="sup-inv-edit"),
    path('sup/rem/<str:hashid>/<str:pk>/', views.supInvRem, name="sup-inv-rem"),
    path('sup/lock/<str:hashid>/<str:pk>/', views.supInvLock, name="sup-inv-lock"),
    path('sup/unlock/<str:hashid>/<str:pk>/', views.supInvUnLock, name="sup-inv-unlock"),
    path('sup/ready/<str:hashid>/<str:pk>/', views.supInvReady, name="sup-inv-ready"),
    # uvip
    path('uvip/list/', views.uvipInvList, name="uvip-inv-list"),
    path('uvip/det/<str:hashid>/', views.uvipInvDet, name="uvip-inv-det"),
    path('uvip/adny/<str:hashid>/', views.uvipInvIsADNY, name="uvip-inv-isadn-y"),
    path('uvip/adnn/<str:hashid>/', views.uvipInvIsADNN, name="uvip-inv-isadn-n"),
    path('inv/adn/<str:pk>/<str:page>/', views.uvipInvADN, name="uvip-inv-adn"),
    # gab
    path('gab/list/', views.gabInvList, name="gab-inv-list"),
    path('gab/det/<str:hashid>/', views.gabInvDet, name="gab-inv-det"),
    path('gab/inv/<str:pk>/', views.gabInvAppr, name="gab-inv-appr"),
    # dgaf
    path('dgaf/list/', views.dgafInvList, name="dgaf-inv-list"),
    path('dgaf/det/<str:hashid>/', views.dgafInvDet, name="dgaf-inv-det"),
    # dna
    path('dna/list/', views.dnaInvList, name="dna-inv-list"),
    path('dna/det/<str:hashid>/', views.dnaInvDet, name="dna-inv-det"),
    # dnof
    path('dnof/list/', views.dnofInvList, name="dnof-inv-list"),
    path('dnof/det/<str:hashid>/', views.dnofInvDet, name="dnof-inv-det"),
    ### CERT
    path('uvip/cert/add/<str:hashid>/', views.uvipCertAdd, name="uvip-cert-add"),
    path('uvip/cert/edit/<str:hashid>/', views.uvipCertEdit, name="uvip-cert-edit"),
    path('uvip/cert/det/<str:hashid>/', views.uvipCertDet, name="uvip-cert-det"),
    path('uvip/cert/rem/<str:pk>/', views.uvipCertRem, name="uvip-cert-rem"),
    path('uvip/cert/lock/<str:pk>/', views.uvipCertLock, name="uvip-cert-lock"),
    ### RECOM
    path('uvip/recom/det/<str:hashid>/', views.uvipRecomDet, name="uvip-recom-det"),
    path('uvip/recom/add/<str:hashid>/', views.uvipRecomAdd, name="uvip-recom-add"),
    path('uvip/recom/edit/<str:hashid>/', views.uvipRecomEdit, name="uvip-recom-edit"),
    path('uvip/recom/rem/<str:pk>/', views.uvipRecomRem, name="uvip-recom-rem"),
    path('uvip/recom/lock/<str:pk>/', views.uvipRecomLock, name="uvip-recom-lock"),
    ###
    path('inv/pdf/<str:hashid>/', views.InvPDF, name="inv-pdf"),
    path('cert/pdf/<str:hashid>/', views.CertPDF, name="cert-pdf"),
    path('recom/pdf/<str:hashid>/', views.RecomPDF, name="recom-pdf"),
    ###
    path('all/inv/list/', views.allInvList, name="all-inv-list"),
    path('all/inv/det/<str:hashid>/', views.allInvDet, name="all-inv-det"),
    path('hist/inv/list/', views.histInvList, name="hist-inv-list"),
    path('hist/inv/det/<str:hashid>/', views.histInvDet, name="hist-inv-det"),
    path('hist/inv/year/<str:year>/', views.histInvYear, name="hist-inv-year"),
    ### OP Recom
    path('op/recom/cont/list/', views.opRecomContList, name="op-recom-cont-list"),
    path('op/recom/list/<str:hashid>/', views.opRecomList, name="op-recom-list"),
    path('op/recom/add2/<str:hashid>/', views.opRecomAdd, name="op-recom-add"),
    path('op/recom/edit2/<str:hashid>/<str:pk>/', views.opRecomEdit, name="op-recom-edit"),
    path('op/recom/rem2/<str:hashid>/<str:pk>/', views.opRecomRem, name="op-recom-rem"),
    path('op/recom/lock2/<str:hashid>/<str:pk>/', views.opRecomLock, name="op-recom-lock"),

]