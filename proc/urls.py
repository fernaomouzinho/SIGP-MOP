from django.urls import path
from . import views

urlpatterns = [
    ### DNA
    path('list/', views.dnaProcList, name="dna-proc-list"),
    path('add/', views.dnaProcAdd, name="dna-proc-add"),
    path('edit/<str:hashid>/', views.dnaProcEdit, name="dna-proc-edit"),
    path('detail/<str:hashid>/', views.dnaProcDet, name="dna-proc-det"),
    path('rem/<str:hashid>/', views.dnaProcRem, name="dna-proc-rem"),
    path('lock/<str:hashid>/', views.dnaProcLock, name="dna-proc-lock"),
    #
    path('comp/add/<str:hashid>/', views.dnaProcCompAdd, name="dna-proc-comp-add"),
    path('comp/edit/<str:hashid>/', views.dnaProcCompEdit, name="dna-proc-comp-edit"),
    path('comp/rem/<str:hashid>/', views.dnaProcCompRem, name="dna-proc-comp-rem"),
    path('comp/win/<str:hashid>/', views.dnaProcCompWin, name="dna-proc-comp-win"),
    # let
    path('let/add/<str:hashid>/<str:page>/', views.ProcLetAdd, name="proc-let-add"),
    path('let/edit/<str:hashid>/<str:page>/', views.ProcLetEdit, name="proc-let-edit"),
    path('let/rem/<str:pk>/<str:page>/', views.ProcLetRem, name="proc-let-rem"),
    #
    path('track/edit/<str:hashid>/<str:pk>/', views.dnaProcTrackEdit, name="dna-proc-track-edit"),
    # req
    path('dna/req/list/', views.dnaProcReqList, name="dna-proc-req-list"),
    path('dna/req/det/<str:hashid>/', views.dnaProcReqDet, name="dna-proc-req-det"),
    path('dna/req/start/<str:pk>/', views.dnaProcReqStart, name="dna-proc-req-start"),
    path('dna/req/end/<str:pk>/', views.dnaProcReqEnd, name="dna-proc-req-end"),
    path('dna/req/next/<str:pk>/', views.dnaProcReqNext, name="dna-proc-req-next"),
    path('dna/req/in/<str:pk>/', views.dnaProcReqIn, name="dna-proc-req-in"),
    # res
    path('dna/res/list/', views.dnaProcResList, name="dna-proc-res-list"),
    path('dna/res/det/<str:hashid>/', views.dnaProcResDet, name="dna-proc-res-det"),
    path('dna/res/start/<str:pk>/', views.dnaProcResStart, name="dna-proc-res-start"),
    path('dna/res/end/<str:pk>/', views.dnaProcResEnd, name="dna-proc-res-end"),
    path('dna/res/next/<str:pk>/', views.dnaProcResNext, name="dna-proc-res-next"),
    path('dna/res/in/<str:pk>/', views.dnaProcResIn, name="dna-proc-res-in"),
    ### DGAF
    path('dgaf/list/', views.dgafProcList, name="dgaf-proc-list"),
    path('dgaf/det/<str:hashid>/', views.dgafProcDet, name="dgaf-proc-det"),
    # req
    path('dgaf/req/list/', views.dgafProcReqList, name="dgaf-proc-req-list"),
    path('dgaf/req/det/<str:hashid>/', views.dgafProcReqDet, name="dgaf-proc-req-det"),
    path('dgaf/req/in1/<str:pk>/', views.dgafProcReqIn1, name="dgaf-proc-req-in1"),
    path('dgaf/req/next1/<str:pk>/', views.dgafProcReqNext1, name="dgaf-proc-req-next1"),
    path('dgaf/req/nextdnof/<str:pk>/', views.dgafProcReqNextDNOF, name="dgaf-proc-req-nextdnof"),
    path('dgaf/req/indnof/<str:pk>/', views.dgafProcReqInDNOF, name="dgaf-proc-req-indnof"),
    path('dgaf/req/in2/<str:pk>/', views.dgafProcReqIn2, name="dgaf-proc-req-in2"),
    path('dgaf/req/next2/<str:pk>/', views.dgafProcReqNext2, name="dgaf-proc-req-next2"),
    # res
    path('dgaf/res/list/', views.dgafProcResList, name="dgaf-proc-res-list"),
    path('dgaf/res/det/<str:hashid>/', views.dgafProcResDet, name="dgaf-proc-res-det"),
    path('dgaf/res/in1/<str:pk>/', views.dgafProcResIn1, name="dgaf-proc-res-in1"),
    path('dgaf/res/next1/<str:pk>/', views.dgafProcResNext1, name="dgaf-proc-res-next1"),
    path('dgaf/res/in2/<str:pk>/', views.dgafProcResIn2, name="dgaf-proc-res-in2"),
    path('dgaf/res/next2/<str:pk>/', views.dgafProcResNext2, name="dgaf-proc-res-next2"),
    ### Gab
    path('gab/list/', views.gabProcList, name="gab-proc-list"),
    path('gab/det/<str:hashid>/', views.gabProcDet, name="gab-proc-det"),
    # req
    path('gab/req/list/', views.gabProcReqList, name="gab-proc-req-list"),
    path('gab/req/det/<str:hashid>/', views.gabProcReqDet, name="gab-proc-req-det"),
    path('gab/req/back/<str:hashid>/', views.gabProcReqBack, name="gab-proc-req-back"),
    path('gab/req/in/<str:pk>/', views.gabProcReqIn, name="gab-proc-req-in"),
    path('gab/req/appr/<str:pk>/', views.gabProcReqAppr, name="gab-proc-req-appr"),
    path('gab/req/next/<str:pk>', views.gabProcReqNext, name="gab-proc-req-next"),
    # res
    path('gab/res/list/', views.gabProcResList, name="gab-proc-res-list"),
    path('gab/res/det/<str:hashid>/', views.gabProcResDet, name="gab-proc-res-det"),
    path('gab/res/back/<str:hashid>/', views.gabProcResBack, name="gab-proc-res-back"),
    path('gab/res/in/<str:pk>/', views.gabProcResIn, name="gab-proc-res-in"),
    path('gab/res/appr/<str:pk>/', views.gabProcResAppr, name="gab-proc-res-appr"),
    path('gab/res/next/<str:pk>', views.gabProcResNext, name="gab-proc-res-next"), 
    ### div
    path('div/list/', views.divProcList, name="div-proc-list"),
    path('div/det/<str:hashid>/', views.divProcDet, name="div-proc-det"),
    ### FILES
    path('file/list/<str:hashid>/', views.dnaProcFileList, name="dna-proc-file-list"),
    path('file/add/<str:hashid>/', views.dnaProcFileAdd, name="min-proc-file-add"),
    path('file/edit/<str:hashid>/<str:hashid2>/', views.dnaProcFileEdit, name="min-proc-file-edit"),
    path('file/rem/<str:hashid>/<str:pk>/', views.dnaProcFileRem, name="min-proc-file-rem"),
    path('file/lock/<str:hashid>/<str:pk>/', views.dnaProcFileLock, name="min-proc-file-lock"),
    ### PDF
    path('let/pdf/<str:pk>/', views.ProcLetPDF, name="proc-let-pdf"),
    path('file/pdf/<str:pk>/', views.ProcFilePDF, name="proc-file-pdf"),
]