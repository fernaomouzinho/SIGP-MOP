from django.urls import path
from . import views

urlpatterns = [
	### DGAF
	path('dgaf/cpvreq/list/', views.notifDGAFCPVReqList, name="notif-dgaf-cpvreq-list"),
	path('dgaf/cpv/list/', views.notifDGAFCPVList, name="notif-dgaf-cpv-list"),
	path('dgaf/po/list/', views.notifDGAFPOList, name="notif-dgaf-po-list"),
	path('dgaf/po/det/<str:hashid>/', views.notifDGAFPODet, name="notif-dgaf-po-det"),
	path('dgaf/proc/list/', views.notifDGAFProcList, name="notif-dgaf-proc-list"),
	path('dgaf/inv/list/', views.notifDGAFInvList, name="notif-dgaf-inv-list"),
	path('dgaf/inv/det/<str:hashid>/', views.notifDGAFInvDet, name="notif-dgaf-inv-det"),
	path('dgaf/badge/', views.notifbadgeDGAF.as_view()),
	path('dgaf/cpvreq/', views.notifDGAFCPVReq.as_view()),
	path('dgaf/cpv/', views.notifDGAFCPV.as_view()),
	path('dgaf/po/', views.notifDGAFPO.as_view()),
	path('dgaf/proc/', views.notifDGAFProc.as_view()),
	path('dgaf/inv/', views.notifDGAFInv.as_view()),
	### DNOF
	path('dnof/cpvreq/list/', views.notifDNOFCPVReqList, name="notif-dnof-cpvreq-list"),
	path('dnof/cpv/list/', views.notifDNOFCPVList, name="notif-dnof-cpv-list"),
	path('dnof/inv/list/', views.notifDNOFInvList, name="notif-dnof-inv-list"),
	path('dnof/inv/det/<str:hashid>/', views.notifDNOFInvDet, name="notif-dnof-inv-det"),
	path('dnof/badge/', views.notifbadgeDNOF.as_view()),
	path('dnof/cpvreq/', views.notifDNOFCPVReq.as_view()),
	path('dnof/cpv/', views.notifDNOFCPV.as_view()),
	path('dnof/inv/', views.notifDNOFInv.as_view()),
 
    ### DNOF-BO
    path('dnofbo/ev/list/', views.notifDNOFBOEvList, name="notif-dnof-bo-ev-list"),
    path('dnofbo/badge/', views.notifbadgeDNOFBO.as_view()),
    path('dnofbo/ev/', views.notifDNOFBOEv.as_view()),
 
    
	### DNA
	path('dna/cpv/list/', views.notifDNACPVList, name="notif-dna-cpv-list"),
	path('dna/po/list/', views.notifDNAPOList, name="notif-dna-po-list"),
	path('dna/eval/list/', views.notifDNAEvalList, name="notif-dna-eval-list"),
	path('dna/proc/list/', views.notifDNAProcList, name="notif-dna-proc-list"),
	path('dna/inv/list/', views.notifDNAInvList, name="notif-dna-inv-list"),
	path('dna/inv/det/<str:hashid>/', views.notifDNAInvDet, name="notif-dna-inv-det"),
	path('dna/badge/', views.notifbadgeDNA.as_view()),
	path('dna/cpv/', views.notifDNACPV.as_view()),
	path('dna/po/', views.notifDNAPO.as_view()),
	path('dna/eval/', views.notifDNAEval.as_view()),
	path('dna/proc/', views.notifDNAProc.as_view()),
	path('dna/inv/', views.notifDNAInv.as_view()),
	### UVIP
	path('uvip/eval/list/', views.notifUVIPEvalList, name="notif-uvip-eval-list"),
	path('uvip/inv/list/', views.notifUVIPInvList, name="notif-uvip-inv-list"),
	path('uvip/inv/det/<str:hashid>/', views.notifUVIPInvDet, name="notif-uvip-inv-det"),
	path('uvip/badge/', views.notifbadgeUVIP.as_view()),
	path('uvip/eval/', views.notifUVIPEval.as_view()),
	path('uvip/inv/', views.notifUVIPInv.as_view()),
 
 
	### GAB
	path('gab/cpv/list/', views.notifGabCPVList, name="notif-gab-cpv"),
	path('gab/eval/list/', views.notifGabEvalList, name="notif-gab-eval-list"),
	path('gab/proc/list/', views.notifGabProcList, name="notif-gab-proc"),
	path('gab/inv/list/', views.notifGabInvList, name="notif-gab-inv-list"),
	path('gab/inv/det/<str:hashid>/', views.notifGabInvDet, name="notif-gab-inv-det"),
	path('gab/badge/', views.notifbadgeGab.as_view()),
	path('gab/cpv/', views.notifGabCPV.as_view()),
	path('gab/eval/', views.notifGabEval.as_view()),
	path('gab/proc/', views.notifGabProc.as_view()),
	path('gab/inv/', views.notifGabInv.as_view()),
	### SUP
	path('sup/inv/list/', views.notifSUPInvList, name="notif-sup-inv-list"),
	path('sup/badge/', views.notifbadgeSUP.as_view()),
	path('sup/inv/', views.notifSUPInv.as_view()),
	### DIV
	path('div/proj/list/', views.notifDIVProjList, name="notif-div-proj-list"),
	path('div/badge/', views.notifbadgeDIV.as_view()),
	path('div/proj/', views.notifDIVpp.as_view()),
 
	path('div/eval/', views.notifDIVEval.as_view()),
	# path('div/eval/disp/', views.notifDIVEvalDisp.as_view()),
	# path('div/inv/disp/', views.notifDIVInvDisp.as_view()),
	# path('div/ver/', views.notifDIVVer.as_view()),
	# path('div/inv/', views.notifDIVInv.as_view()),
	path('div/eval/list/', views.notifDIVEvalList, name="notif-div-eval-list"),
	# path('div/eval/disp/list/', views.notifDIVEvalDispList, name="notif-div-eval-disp"),
	# path('div/inv/disp/list/', views.notifDIVInvDispList, name="notif-div-inv-disp"),
	# path('div/ver/list/', views.notifDIVVerList, name="notif-div-ver-list"),
	# path('div/inv/list/', views.notifDIVInvList, name="notif-div-inv-list"),
	### DEP
	# path('dep/badge/', views.notifbadgeDEP.as_view()),
	# path('dep/ver/', views.notifDEPVer.as_view()),
	# path('dep/ver/list/', views.notifDEPVerList, name="notif-dep-ver-list"),
	### UVIP
	path('uvip/badge/', views.notifbadgeUVIP.as_view()),
	path('uvip/ver/', views.notifUVIPVer.as_view()),
	path('uvip/ver/list/', views.notifUVIPVerList, name="notif-uvip-ver-list"),
    
    path('uvip/insp/', views.notifUVIPInsp.as_view()),
	path('uvip/insp/list/', views.notifUVIPInspList, name="notif-uvip-insp-list"),
 
	### SEC
	path('sec/badge/', views.notifbadgeSEC.as_view()),
	path('sec/ver/', views.notifSECVer.as_view()),
	path('sec/ver/list/', views.notifSECVerList, name="notif-sec-ver-list"),
	
    path('sec/insp/', views.notifSECInsp.as_view()),
	path('sec/insp/list/', views.notifSECInspList, name="notif-sec-insp-list"),
 
	### ENG
	path('eng/ver/list/', views.notifENGVerList, name="notif-eng-ver-list"),
    path('eng/insp/list/', views.notifENGInspList, name="notif-eng-insp-list"),
	path('eng/badge/', views.notifbadgeENG.as_view()),
	path('eng/ver/', views.notifENGVer.as_view()),
 	path('eng/insp/', views.notifENGInsp.as_view()),
]