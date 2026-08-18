from django.urls import path
from . import views

urlpatterns = [
    ### DIV
    # eval
    path('div/list/', views.divEvalList, name="div-eval-list"),
    path('div/add/', views.divEvalAdd, name="div-eval-add"),
    path('div/edit/<str:hashid>/', views.divEvalEdit, name="div-eval-edit"),
    path('div/detail/<str:hashid>/', views.divEvalDetail, name="div-eval-det"),
    path('div/rem/<str:hashid>/', views.divEvalRem, name="div-eval-rem"),
    path('div/send/<str:hashid>/', views.divEvalSend, name="div-eval-send"),
    path('uvip/adn/<str:pk>/<str:page>/', views.uvipEvalADN, name="uvip-eval-adn"),
   
    #
    path('div/file/add/<str:hashid>/', views.divEvalFileAdd, name="div-eval-file-add"),
    path('div/file/edit/<str:hashid>/<str:pk>/', views.divEvalFileEdit, name="div-eval-file-edit"),
    path('div/file/rem/<str:hashid>/<str:pk>/', views.divEvalFileRem, name="div-eval-file-rem"),
    
    # uvip
    path('uvip/list/', views.uvipEvalList, name="uvip-eval-list"),
    path('uvip/list/<str:hashid>/', views.uvipEvalList2, name="uvip-eval-list2"),
    path('uvip/det/<str:hashid>/', views.uvipEvalDetail, name="uvip-eval-det"),
    path('uvip/let/add/<str:hashid>/', views.uvipEvalLetAdd, name="uvip-eval-let-add"),
    path('uvip/let/edit/<str:hashid>/', views.uvipEvalLetEdit, name="uvip-eval-let-edit"),
    path('uvip/let/rem/<str:pk>/', views.uvipEvalLetRem, name="uvip-eval-let-rem"),
    path('uvip/in/<str:pk>/', views.uvipEvalIn, name="uvip-eval-in"),
    path('uvip/ver/start/<str:hashid>/', views.uvipEvalVerStart, name="uvip-eval-ver-start"),
    path('uvip/ver/end/<str:hashid>/', views.uvipEvalVerEnd, name="uvip-eval-ver-end"),
    
    path('uvip/next1/<str:pk>/', views.uvipEvalNext1, name="uvip-eval-next1"),
    path('uvip/adnin/<str:pk>/', views.uvipEvalADNIn, name="uvip-eval-adnin"),
    path('uvip/adnin/back/dev/<str:hashid>/', views.uvipEvalLetADNBackDev, name="uvip-adn-eval-back-dev"),
    path('uvip/adnin/back/dev/edit/<str:hashid>/', views.uvipEvalLetADNBackDevEdit, name="uvip-adn-eval-back-dev-edit"),
    path('uvip/adnin/back/res/<str:hashid>/', views.uvipEvalLetADNBackRes, name="uvip-adn-eval-back-res"),
    path('uvip/adnin/back/res/edit/<str:hashid>/', views.uvipEvalLetADNBackResEdit, name="uvip-adn-eval-back-res-edit"),
    path('uvip/next2/<str:pk>/', views.uvipEvalNext2, name="uvip-eval-next2"),
    path('uvip/adninreviw/<str:pk>/', views.uvipEvalNext2, name="uvip-eval-next2"),
    
    #
    path('fi/uvip/next/<str:pk>/', views.uvipEvalFINext, name="uvip-evalfi-next"),
    path('fi/uvip/in3/<str:pk>/', views.uvipEvalFIIn3, name="uvip-evalfi-in3"),
    path('fi/uvip/next1/<str:pk>/', views.uvipEvalFINext1, name="uvip-evalfi-next1"),
    path('fi/uvip/in4/<str:pk>/', views.uvipEvalFIIn4, name="uvip-evalfi-in4"),
    path('fi/uvip/next2/<str:pk>/', views.uvipEvalFINext2, name="uvip-evalfi-next2"),
    path('fi/uvip/next3/<str:pk>/', views.uvipEvalFINext3, name="uvip-evalfi-next3"),
    path('fi/uvip/in5/<str:pk>/', views.uvipEvalFIIn5, name="uvip-evalfi-in5"),
    path('fi/uvip/next4/<str:pk>/', views.uvipEvalFINext4, name="uvip-evalfi-next4"),
    path('fi/uvip/next5/<str:pk>/', views.uvipEvalFINext5, name="uvip-evalfi-next5"),
    path('fi/uvip/in6/<str:pk>/', views.uvipEvalFIIn6, name="uvip-evalfi-in6"),
    path('fi/uvip/next6/<str:pk>/', views.uvipEvalFINext6, name="uvip-evalfi-next6"),
    
    
    
    
    # path('fi/uvip/next4/<str:pk>/', views.uvipEvalFINext4, name="uvip-evalfi-next4"),
    # path('fi/uvip/next5/<str:pk>/', views.uvipEvalFINext5, name="uvip-evalfi-next5"),
    #
    # gab
    path('gab/list/', views.gabEvalList, name="gab-eval-list"),
    path('gab/det/<str:hashid>/', views.gabEvalDetail, name="gab-eval-det"),
    path('gab/back/<str:hashid>/', views.gabEvalBack, name="gab-eval-back"),
    path('gab/let/add/<str:hashid>/', views.gabEvalLetAdd, name="gab-eval-let-add"),
    path('gab/let/edit/<str:hashid>/', views.gabEvalLetEdit, name="gab-eval-let-edit"),
    path('gab/let/rem/<str:pk>/', views.gabEvalLetRem, name="gab-eval-let-rem"),
    
   
    path('gab/in/<str:pk>/', views.gabEvalIn, name="gab-eval-in"),  #Presija hare fila fali tanba la eziste iha view
    
    path('gab/appr/<str:pk>/', views.gabEvalAppr, name="gab-eval-appr"),
    path('gab/let/appr/<str:pk>/', views.gabEvalLetAppr, name="gab-eval-let-appr"),
    path('gab/end/<str:pk>/', views.gabEvalEnd, name="gab-eval-end"),
    
    # path('gab/let/return/<str:pk>/', views.gabEvalReturn, name="gab-eval-return"),
    path('gab/let/return/add/<str:hashid>/', views.gabEvalReturnAdd, name="gab-eval-return-add"),
    
    #
    path('fi/gab/in1/<str:pk>/', views.gabEvalFIIn1, name="gab-evalfi-in1"),
    path('fi/gab/next1/<str:pk>/', views.gabEvalFINext1, name="gab-evalfi-next1"),
    path('fi/gab/in2/<str:pk>/', views.gabEvalFIIn2, name="gab-evalfi-in2"),
    path('fi/gab/next2/<str:pk>/', views.gabEvalFINext2, name="gab-evalfi-next2"),
    path('fi/gab/in3/<str:pk>/', views.gabEvalFIIn3, name="gab-evalfi-in3"),
    path('fi/gab/next3/<str:pk>/', views.gabEvalFINext3, name="gab-evalfi-next3"),
    path('fi/gab/next4/<str:pk>/', views.gabEvalFINext4, name="gab-evalfi-next4"),
    path('fi/gab/in4/<str:pk>/', views.gabEvalFIIn4, name="gab-evalfi-in4"),
    path('fi/gab/next5/<str:pk>/', views.gabEvalFINext5, name="gab-evalfi-next5"),
    path('fi/gab/in5/<str:pk>/', views.gabEvalFIIn5, name="gab-evalfi-in5"),
    path('fi/gab/next6/<str:pk>/', views.gabEvalFINext6, name="gab-evalfi-next6"),
    path('fi/gab/next7/<str:pk>/', views.gabEvalFINext7, name="gab-evalfi-next7"),
    
    path('fi/gab/return/add/<str:hashid>/', views.gabEvalFIReturnAdd, name="gab-evalfi-return-add"),
    path('fi/gab/result/add/<str:hashid>/', views.gabEvalFIResultAdd, name="gab-evalfi-result-add"),
    
    
    # dna
    path('dna/list/', views.dnaEvalList, name="dna-eval-list"),
    path('dna/det/<str:hashid>/', views.dnaEvalDetail, name="dna-eval-det"),
    
    ### pdf
    path('file/pdf/boq/<str:pk>/', views.EvalFilePDFBOQ, name="eval-file-pdf-boq"),
    path('file/pdf/design/<str:pk>/', views.EvalFilePDFDesign, name="eval-file-pdf-design"),
    path('file/pdf/spec/<str:pk>/', views.EvalFilePDFSpec, name="eval-file-pdf-spec"),
    path('file/pdf/mapq/<str:pk>/', views.EvalFilePDFMapQ, name="eval-file-pdf-mapq"),
    path('file/pdf/other/<str:pk>/', views.EvalFilePDFDocOther, name="eval-file-pdf-other"),
    path('let/pdf/<str:hashid>/', views.EvalLetPDF, name="eval-let-pdf"),
    
    path('file/pdf/adn/rs/<str:pk>/', views.EvalFileAdnPDFRS, name="eval-file-adn-pdf-rs"),
    path('file/pdf/adn/boq/<str:pk>/', views.EvalFileAdnPDFBOQ, name="eval-file-pdf-adn-boq"),
    path('file/pdf/adn/design/<str:pk>/', views.EvalFileAdnPDFDesign, name="eval-file-pdf-adn-design"),
    path('file/pdf/adn/spec/<str:pk>/', views.EvalFileAdnPDFSpec, name="eval-file-pdf-adn-spec"),
    path('file/pdf/adn/mapq/<str:pk>/', views.EvalFileAdnPDFMapQ, name="eval-file-pdf-adn-mapq"),
    path('file/pdf/adn/other/<str:pk>/', views.EvalFileAdnPDFDocOther, name="eval-file-pdf-adn-other"),  
]