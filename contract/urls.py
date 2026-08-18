from django.urls import path
from . import views

urlpatterns = [
    ### DNA
    path('dna/list/', views.dnaContList, name="dna-cont-list"),
    path('dna/det/<str:hashid>/', views.dnaContDet, name="dna-cont-det"),    
    path('dna/add/', views.dnaContAdd, name="dna-cont-add"),
    path('dna/edit/<str:hashid>/', views.dnaContEdit, name="dna-cont-edit"),
    path('dna/rem/<str:pk>/', views.dnaContRem, name="dna-cont-rem"),
    path('dna/lock/<str:hashid>/', views.dnaContLock, name="dna-cont-lock"),
    path('dna/unlock/<str:hashid>/', views.dnaContUnLock, name="dna-cont-unlock"),
    path('dna/ready/<str:hashid>/', views.dnaContReady, name="dna-cont-ready"),
    path('dna/complete/<str:hashid>/', views.dnaContComplete, name="dna-cont-complete"),
    path('dna/status/edit/<str:hashid>/', views.dnaContStatusEdit, name="dna-cont-status-edit"),
    path('dna/stop/<str:hashid>/', views.dnaContStopEdit, name="dna-cont-stop"),
    path('dna/year/edit/<str:pk>/', views.dnaContYearEdit, name="dna-contyear-edit"),
    #
    path('dna/comp/add/<str:hashid>/', views.dnaContCompAdd, name="dna-cont-comp-add"),
    path('dna/comp/edit/<str:hashid>/<str:pk>/', views.dnaContCompEdit, name="dna-cont-comp-edit"),
    path('dna/comp/rem/<str:hashid>/<str:pk>/', views.dnaContCompRem, name="dna-cont-comp-rem"),
    path('dna/file/add/<str:hashid>/', views.dnaContFileAdd, name="dna-cont-file-add"),
    path('dna/file/edit/<str:hashid>/<str:pk>/', views.dnaContFileEdit, name="dna-cont-file-edit"),
    path('dna/file/rem/<str:hashid>/<str:pk>/', views.dnaContFileRem, name="dna-cont-file-rem"),
    # AMEND
    path('amend/per/list/', views.AmendPerList, name="amend-per-list"),
    path('amend/per/det/<str:hashid>/', views.AmendPerDet, name="amend-per-det"),
    path('amend/per/add/<str:hashid>/', views.AmendPerAdd, name="amend-per-add"),
    path('amend/per/edit/<str:hashid>/<str:pk>/', views.AmendPerEdit, name="amend-per-edit"),
    path('amend/per/rem/<str:hashid>/<str:pk>/', views.AmendPerRem, name="amend-per-rem"),
    path('amend/per/conf/<str:hashid>/<str:pk>/', views.AmendPerConf, name="amend-per-conf"),
    path('amend/am/list/', views.AmendAmList, name="amend-am-list"),
    path('amend/am/det/<str:hashid>/', views.AmendAmDet, name="amend-am-det"),
    path('amend/am/add/<str:hashid>/', views.AmendAmAdd, name="amend-am-add"),
    path('amend/am/edit/<str:hashid>/<str:pk>/', views.AmendAmEdit, name="amend-am-edit"),
    path('amend/am/rem/<str:hashid>/<str:pk>/', views.AmendAmRem, name="amend-am-rem"),
    path('amend/am/conf/<str:hashid>/<str:pk>/', views.AmendAmConf, name="amend-am-conf"),
    path('deduc/am/list/', views.DeducList, name="deduc-list"),
    path('deduc/det/<str:hashid>/', views.DeducDet, name="deduc-det"),
    path('deduc/add/<str:hashid>/', views.DeducAdd, name="deduc-add"),
    path('deduc/edit/<str:hashid>/<str:pk>/', views.DeducEdit, name="deduc-edit"),
    path('deduc/rem/<str:hashid>/<str:pk>/', views.DeducRem, name="deduc-rem"),
    path('deduc/conf/<str:hashid>/<str:pk>/', views.DeducConf, name="deduc-conf"),
    ### ALL
    path('list/', views.ContList, name="cont-list"),
    path('det/<str:hashid>/', views.ContDet, name="cont-det"),
    path('monitor/list/', views.ContMonitorList, name="cont-monitor-list"),
    #
    path('sup/list/', views.supContList, name="sup-cont-list"),
    ##
    path('pdf/<str:pk>/', views.ContPDF, name="cont-pdf"),
    ###
    path('c/proj/list/', views.compContList, name="comp-proj-list"),
    path('c/proj/det/<str:hashid>/', views.compContDet, name="comp-proj-det"),
    
    # Atualiza Status
    path('dna/upate/cont/proj/status/', views.dnaContUpdataEstatus, name="dna-cont-proj-update-status"),

]