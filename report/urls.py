from django.urls import path
from . import views

urlpatterns = [
    path('dash/', views.rProjDash, name="r-proj-dash"),
    path('dash/<str:year>/', views.rProjYearDash, name="r-proj-year-dash"),
    #
    path('proj/list/', views.rProjList, name="r-proj-list"),
    path('proj/year/list/<str:year>/', views.rProjYearList, name="r-proj-year-list"),
    path('proj/statusp/list/<str:pk>/', views.rProjStatusPList, name="r-proj-statusp-list"),
    path('proj/statusp/year/list/<str:pk>/<str:year>/', views.rProjStatusPYearList, name="r-proj-statusp-year-list"),
    path('proj/status/list/<str:pk>/', views.rProjStatusList, name="r-proj-status-list"),
    path('proj/status/year/list/<str:pk>/<str:year>/', views.rProjStatusYearList, name="r-proj-status-year-list"),
    #
    path('imp/list/', views.rImpList, name="r-imp-list"),
    path('imp/year/list/<str:year>/', views.rImpYearList, name="r-imp-year-list"),
    path('imp/status/list/<str:pk>/', views.rImpStatusList, name="r-imp-status-list"),
    path('imp/status/year/list/<str:pk>/<str:year>/', views.rImpStatusYearList, name="r-imp-status-year-list"),
    #
    path('pmopcat/list/<str:pk>/', views.rPMopCatList, name="r-pmopcat-list"),
    path('pmopcat/year/list/<str:pk>/<str:year>/', views.rPMopCatYearList, name="r-pmopcat-year-list"),
    path('pcat/list/<str:pk>/', views.rPCatList, name="r-pcat-list"),
    path('pcat/year/list/<str:pk>/<str:year>/', views.rPCatYearList, name="r-pcat-year-list"),
    path('pcap/list/<str:pk>/', views.rPCapList, name="r-pcap-list"),
    path('pcap/year/list/<str:pk>/<str:year>/', views.rPCapYearList, name="r-pcap-year-list"),
    path('psec/list/<str:pk>/', views.rPSecList, name="r-psec-list"),
    path('psec/year/list/<str:pk>/<str:year>/', views.rPSecYearList, name="r-psec-year-list"),
    #
    path('proj/mun/summary/', views.rPMunSum, name="r-proj-mun-sum"),
    path('proj/mun/list/<str:pk>/', views.rPMunList, name="r-proj-mun-list"),
    path('proj/mun/year/<str:pk>/<str:year>/', views.rPMunYearList, name="r-proj-mun-year"),
    #
    path('proj/type/summary/', views.rPTypeSum, name="r-proj-type-sum"),
    path('proj/type/list/<str:pk>/', views.rPTypeList, name="r-proj-type-list"),
    path('proj/type/year/<str:pk>/<str:year>/', views.rPTypeYearList, name="r-proj-type-year"),
    ### COMP
    path('comp/proj/sum/', views.rCompProjSum, name="r-comp-proj-sum"),
    path('comp/proj/list/<str:pk>/', views.rCompProjList, name="r-comp-proj-list"),
    path('comp/proj/status/list/<str:pk>/<str:pk2>/', views.rCompProjStatusList, name="r-comp-proj-status-list"),
    path('comp/proj/year/list/<str:pk>/<str:year>/', views.rCompProjYearList, name="r-comp-proj-year-list"),
    path('comp/search/', views.rCompSearch, name="r-comp-search"),
    path('cont/limit/list/', views.rContLimitList, name="r-cont-limit-list"),
    ### RAW DATA
    path('raw/data/', views.rRawData, name="r-raw-data"),
    path('raw/data/cpv/<str:hashid>/', views.rRawDataCPV, name="r-raw-data-cpv"),
    path('raw/data/prt/<str:hashid>/', views.rRawDataPRT, name="r-raw-data-prt"),
    path('raw/data/recom/<str:hashid>/', views.rRawDataRecom, name="r-raw-data-recom"),
    path('raw/data/tpo/<str:hashid>/', views.rRawDataTPO, name="r-raw-data-tpo"),
    #
    path('div/list/', views.rDivList, name="r-div-list"),
    #
    path('recap/dash/', views.rRecapDash, name="r-recap-dash"),
    path('recap/dash/category/<str:pcat>/', views.rRecapPayPortDet, name="r-recap-pay-port-det"),
    path('recap/dash/category/<str:pcat>/pro/<str:pro>/', views.rRecapPayProjOngDet, name="r-recap-pay-proj-ong-det"),
    
    
    path('recap/dash/total/ver/project/capital/<str:pcat>/<str:stage>/', views.rRecapVerProjList1, name="r-recap-ver-proj-list1"),
    path('recap/dash/total/ver/project/category/<str:pcat>/<str:stage>/', views.rRecapVerProjList2, name="r-recap-ver-proj-list2"),
    path('recap/dash/totals/ver/project/category/<str:pcat>/<str:stage>/', views.rRecapVerProjList3, name="r-recap-ver-proj-list3"),
    
    
    
    
    
    path('recap/dash/total/insp/project/capital/<str:pcat>/<str:stage>/', views.rRecapInspProjList1, name="r-recap-insp-proj-list1"),
    path('recap/dash/total/insp/project/category/<str:pcat>/<str:stage>/', views.rRecapInspProjList2, name="r-recap-insp-proj-list2"),
    path('recap/dash/totals/insp/project/category/<str:pcat>/<str:stage>/', views.rRecapInspProjList3, name="r-recap-insp-proj-list3"),
    
    
    
    
    # path('recap/dash/comp/imp/project/', views.rRecapCompProjSum, name="r-recap-com-imp-proj-sum"),
    #path('recap/cap/all/det/', views.rRecapCapAllDet, name="r-recap-cap-all-det"),
    #path('recap/cap/<str:pk>/det/', views.rRecapCapEachDet, name="r-recap-cap-each-det"),
    #path('recap/dash/year/<str:year>/', views.rRecapDashYear, name="r-recap-dash-year"),
    
]