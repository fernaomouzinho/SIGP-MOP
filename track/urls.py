from django.urls import path
from . import views

urlpatterns = [
    #
    path('cpvreq/list/', views.trackCPVReqList, name="track-cpvreq-list"),
    path('cpvreq/det/<str:hashid>/', views.trackCPVReqDet, name="track-cpvreq-det"),
    path('cpv/list/', views.trackCPVList, name="track-cpv-list"),
    path('cpv/det/<str:hashid>/', views.trackCPVDet, name="track-cpv-det"),
    #
    path('po/list/', views.trackPOList, name="track-po-list"),
    path('po/det/<str:hashid>/', views.trackPODet, name="track-po-det"),
    #
    path('eval/list/', views.trackEvalList, name="track-eval-list"),
    path('eval/div/list/', views.trackdivEvalList, name="track-div-eval-list"),
    path('eval/det/<str:hashid>/', views.trackEvalDet, name="track-eval-det"),
    path('eval/det2/<str:hashid>/', views.trackEvalDet2, name="track-eval-det2"),
    #
    path('proc/list/', views.trackProcList, name="track-proc-list"),
    path('proc/det/<str:hashid>/', views.trackProcDet, name="track-proc-det"),
    #
    path('inv/list/', views.trackInvList, name="track-inv-list"),
    path('inv/det/<str:hashid>/', views.trackInvDet, name="track-inv-det"),
    path('comp/inv/list/', views.compTrackInvList, name="track-comp-inv-list"),
    path('comp/inv/det/<str:hashid>/', views.compTrackInvDet, name="track-comp-inv-det"),
    #
    path('ver/list/', views.trackVerList, name="track-ver-list"),
    path('ver/det/<str:hashid>/', views.trackVerDet, name="track-ver-det"),
    #
    path('insp/list/', views.trackInspList, name="track-insp-list"),
    path('insp/det/<str:hashid>/', views.trackInspDet, name="track-insp-det"),
    ###
    path('cpvreq/just/add/<str:hashid>/', views.CPVReqJustAdd, name="cpvreq-just-add"),
    path('cpvreq/just/edit/<str:hashid>/<str:pk>/', views.CPVReqJustEdit, name="cpvreq-just-edit"),
    path('cpvreq/just/rem/<str:hashid>/<str:pk>/', views.CPVReqJustRem, name="cpvreq-just-rem"),
    #
    path('cpv/just/add/<str:hashid>/', views.CPVJustAdd, name="cpv-just-add"),
    path('cpv/just/edit/<str:hashid>/<str:pk>/', views.CPVJustEdit, name="cpv-just-edit"),
    path('cpv/just/rem/<str:hashid>/<str:pk>/', views.CPVJustRem, name="cpv-just-rem"),
    #
    path('po/just/add/<str:hashid>/', views.POJustAdd, name="po-just-add"),
    path('po/just/edit/<str:hashid>/<str:pk>/', views.POJustEdit, name="po-just-edit"),
    path('po/just/rem/<str:hashid>/<str:pk>/', views.POJustRem, name="po-just-rem"),
    #
    path('eval/just/add/<str:hashid>/', views.EvalJustAdd, name="eval-just-add"),
    path('eval/just/edit/<str:hashid>/<str:pk>/', views.EvalJustEdit, name="eval-just-edit"),
    path('eval/just/rem/<str:hashid>/<str:pk>/', views.EvalJustRem, name="eval-just-rem"),
    #
    path('proc/just/add/<str:hashid>/', views.ProcJustAdd, name="proc-just-add"),
    path('proc/just/edit/<str:hashid>/<str:pk>/', views.ProcJustEdit, name="proc-just-edit"),
    path('proc/just/rem/<str:hashid>/<str:pk>/', views.ProcJustRem, name="proc-just-rem"),
    #
    path('inv/justify/add/<str:hashid>/', views.InvJustifyAdd, name="inv-justify-add"),
    path('inv/justify/edit/<str:hashid>/<str:pk>/', views.InvJustifyEdit, name="inv-justify-edit"),
    path('inv/justify/rem/<str:hashid>/<str:pk>/', views.InvJustifyRem, name="inv-justify-rem"),
    #
    path('ver/justify/add/<str:hashid>/', views.VerJustifyAdd, name="ver-justify-add"),
    path('ver/justify/edit/<str:hashid>/<str:pk>/', views.VerJustifyEdit, name="ver-justify-edit"),
    path('ver/justify/rem/<str:hashid>/<str:pk>/', views.VerJustifyRem, name="ver-justify-rem"),
    
    path('insp/justify/add/<str:hashid>/', views.InspJustifyAdd, name="insp-justify-add"),
    path('insp/justify/edit/<str:hashid>/<str:pk>/', views.InspJustifyEdit, name="insp-justify-edit"),
    path('insp/justify/rem/<str:hashid>/<str:pk>/', views.InspJustifyRem, name="insp-justify-rem"),

]