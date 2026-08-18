from django.urls import path
from . import views

urlpatterns = [
    ### PAY
    path('dna/pay/inv/list/', views.dnaPayInvList, name="dna-pay-inv-list"),
    path('dna/pay/inv/det/<str:hashid>/', views.dnaPayInvDet, name="dna-pay-inv-det"),
    path('dna/add/<str:hashid>/', views.dnaPayAdd, name="dna-pay-add"),
    path('dna/edit/<str:hashid>/<str:hashid2>/', views.dnaPayEdit, name="dna-pay-edit"),
    path('dna/rem/<str:hashid>/<str:pk>/', views.dnaPayRem, name="dna-pay-rem"),
    path('dna/lock/<str:hashid>/<str:pk>/', views.dnaPayLock, name="dna-pay-lock"),
    path('dna/unlock/<str:hashid>/<str:pk>/', views.dnaPayUnLock, name="dna-pay-unlock"),
    path('dna/ready/<str:hashid>/<str:pk>/', views.dnaPayReady, name="dna-pay-ready"),
    path('dna/refresh/<str:hashid>/<str:pk>/', views.dnaPayRefresh, name="dna-pay-refresh"),
    #
    path('custom/cont/list/', views.customPayContList, name="custom-pay-cont-list"), 
    path('custom/list/<str:hashid>/', views.customPayList, name="custom-pay-list"), 
    path('custom/add/<str:hashid>/', views.customPayAdd, name="custom-pay-add"),
    path('custom/edit/<str:hashid>/<str:hashid2>/', views.customPayEdit, name="custom-pay-edit"),
    path('custom/rem/<str:hashid>/<str:pk>/', views.customPayRem, name="custom-pay-rem"),
    path('custom/ready/<str:hashid>/<str:pk>/', views.customPayReady, name="custom-pay-ready"),
    path('custom/refresh/<str:hashid>/', views.customPayRefresh, name="custom-pay-refresh"),
    path('custom/deduc/refresh/<str:hashid>/', views.customPayDeducRefresh, name="custom-pay-deduc-refresh"),
    #
    path('fiscal/cont/list/', views.fiscalPayContList, name="fiscal-pay-cont-list"), 
    path('fiscal/year/<str:hashid>/', views.fiscalYearList, name="fiscal-year-list"), 
    path('fiscal/all/<str:hashid>/', views.fiscalPayAll, name="fiscal-pay-all"),
    path('fiscal/list/<str:hashid>/<str:year>/', views.fiscalPayList, name="fiscal-pay-list"), 
    path('fiscal/add/<str:hashid>/<str:year>/', views.fiscalPayAdd, name="fiscal-pay-add"),
    path('fiscal/edit/<str:hashid>/<str:hashid2>/<str:year>/', views.fiscalPayEdit, name="fiscal-pay-edit"),
    path('fiscal/rem/<str:hashid>/<str:pk>/<str:year>/', views.fiscalPayRem, name="fiscal-pay-rem"),
    path('fiscal/ready/<str:hashid>/<str:pk>/<str:year>/', views.fiscalPayReady, name="fiscal-pay-ready"),
    path('fiscal/update/<str:pk>/<str:year>/', views.PayFiscalUpdate, name="pay-fiscal-update"),
    path('fiscal/ena/<str:hashid>/<str:pk>/', views.PayFiscalEna, name="pay-fiscal-ena"),
    path('fiscal/end/<str:hashid>/<str:year>/<str:pk>/', views.PayFiscalEnd, name="pay-fiscal-end"),
    #
    path('all/cont/list/', views.allPayContList, name="all-pay-cont-list"), 
    path('all/list/<str:hashid>/', views.allPayList, name="all-pay-list"), 
    #
    path('cont/update/<str:hashid>/', views.ContPayUpdate, name="cont-pay-update"),
    ###
    path('prog/list/', views.ProgList, name="prog-list"),
    path('prog/year/<str:year>/', views.ProgYearList, name="prog-year"),
    path('prog/phy/list/<str:hashid>', views.PhysicalProgList, name="phy-prog-list"),
    path('prog/phy/list/<str:hashid>/add', views.PhysicalProgAdd, name="phy-prog-add"),   
    path('prog/phy/list/<int:pk>/edit', views.PhysicalProgEdit, name="phy-prog-edit"),   
    
    #Payment Portal
    path("pay/portal/", views.payPortalList, name="pay-portal-list"),
    path("pay/portal/add/", views.payPortalAdd, name="pay-portal-add"),
    path("pay/portal/update/<str:hashid>/", views.payPortalEdit, name="pay-portal-edit"),
    path("pay/portal/delete/<str:hashid>/", views.payPortalDelete, name="pay-portal-delete"), 
]