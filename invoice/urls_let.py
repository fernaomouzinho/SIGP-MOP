from django.urls import path
from . import views

urlpatterns = [
    # sup
    path('sup/add/<str:hashid>/', views.supInvLetAdd, name="sup-inv-let-add"),
    path('div/edit/<str:hashid>/<str:pk>/', views.supInvLetEdit, name="sup-inv-let-edit"),
    path('sup/rem/<str:hashid>/<str:pk>/', views.supInvLetRem, name="sup-inv-let-rem"),
    path('sup/next/<str:pk>/', views.supInvLetNext, name="sup-inv-next"),
    # uvip
    path('uvip/back/<str:hashid>/', views.uvipInvBack, name="uvip-inv-back"),
    path('uvip/in/<str:pk>/', views.uvipInvIn, name="uvip-inv-in"),
    path('uvip/insp/start/<str:hashid>/', views.uvipInvInspStart, name="uvip-inv-insp-start"),
    path('uvip/insp/end/<str:hashid>/', views.uvipInvInspEnd, name="uvip-inv-insp-end"),
    # uvip, gab, dgaf, dna, dnof
    path('add/<str:hashid>/', views.InvLetAdd, name="inv-let-add"),
    path('edit/<str:hashid>/', views.InvLetEdit, name="inv-let-edit"),
    path('rem/<str:pk>/', views.InvLetRem, name="inv-let-rem"),
    # uvip
    path('uvip/next1/<str:pk>/', views.uvipInvNext1, name="uvip-inv-next1"),
    path('uvip/adn/in/<str:pk>/', views.uvipInvADNIn, name="uvip-inv-adn-in"),
    path('uvip/next2/<str:pk>/', views.uvipInvNext2, name="uvip-inv-next2"),
    path('uvip/adnin/back/dev/<str:hashid>/', views.uvipInvLetADNBackDev, name="uvip-adn-inv-back-dev"),
    #path('uvip/adnin/back/dev/edit/<str:hashid>/', views.uvipInvLetADNBackDevEdit, name="uvip-adn-inv-back-dev-edit"),
    path('uvip/adnin/return/dev/<str:hashid>/', views.uvipInvLetADNReturnDev, name="uvip-adn-inv-return-dev"),
    # gab
    path('gab/in/<str:pk>/', views.gabInvIn, name="gab-inv-in"),
    path('gab/back/<str:hashid>/', views.gabInvBack, name="gab-inv-back"),
    path('gab/next1/<str:pk>/', views.gabInvNext1, name="gab-inv-next1"),
    path('gab/next2/<str:pk>/', views.gabInvNext2, name="gab-inv-next2"),
    # dgaf
    path('dgaf/in/<str:pk>/', views.dgafInvIn, name="dgaf-inv-in"),
    path('dgaf/back/<str:hashid>/', views.dgafInvBack, name="dgaf-inv-back"),
    path('dgaf/next/<str:pk>/', views.dgafInvNext, name="dgaf-inv-next"),
    # dna
    path('dna/in/<str:pk>/', views.dnaInvIn, name="dna-inv-in"),
    path('dna/back/<str:hashid>/', views.dnaInvBack, name="dna-inv-back"),
    path('dna/next/<str:pk>/', views.dnaInvNext, name="dna-inv-next"),
    # dnof
    path('dnof/in/<str:pk>/', views.dnofInvIn, name="dnof-inv-in"),
    path('dnof/back/<str:hashid>/', views.dnofInvBack, name="dnof-inv-back"),
    path('dnof/next/<str:pk>/', views.dnofInvNext, name="dnof-inv-next"),
    path('dnof/end/<str:pk>/', views.dnofInvEnd, name="dnof-inv-end"),
    # RELS
    path('cont/list/', views.letContList, name="let-cont-list"),
    path('inv/list/<str:hashid>/', views.letInvList, name="let-inv-list"),
    path('inv/lets/<str:hashid>/', views.letInvLetList, name="let-inv-lets"),
    # # # all pdf
    path('inv/pdf/<str:hashid>/', views.InvLetPDF, name="inv-let-pdf"),
    
]