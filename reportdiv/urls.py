from django.urls import path
from . import views

urlpatterns = [
    path('', views.rdivDash, name="r-div"),
    path('dash/<str:pk>/', views.rdivProjDash, name="r-div-proj-dash"),
    path('dash/<str:pk>/<str:year>/', views.rdivProjYearDash, name="r-div-proj-year-dash"),
    #
    path('proj/list/<str:pk>/', views.rdivProjList, name="r-div-proj-list"),
    path('proj/year/list/<str:pk>/<str:year>/', views.rdivProjYearList, name="r-div-proj-year-list"),
    path('proj/statusp/list/<str:pk>/<str:pk2>/', views.rdivProjStatusPList, name="r-div-proj-statusp-list"),
    path('proj/statusp/year/list/<str:pk>/<str:pk2>/<str:year>/', views.rdivProjStatusPYearList, name="r-div-proj-statusp-year-list"),
    path('proj/status/list/<str:pk>/<str:pk2>/', views.rdivProjStatusList, name="r-div-proj-status-list"),
    path('proj/status/year/list/<str:pk>/<str:pk2>/<str:year>/', views.rdivProjStatusYearList, name="r-div-proj-status-year-list"),
    #
    path('imp/list/<str:pk>/', views.rdivImpList, name="r-div-imp-list"),
    path('imp/year/list/<str:pk>/<str:year>/', views.rdivImpYearList, name="r-div-imp-year-list"),
    path('imp/status/list/<str:pk>/<str:pk2>/', views.rdivImpStatusList, name="r-div-imp-status-list"),
    path('imp/status/year/list/<str:pk>/<str:pk2>/<str:year>/', views.rdivImpStatusYearList, name="r-div-imp-status-year-list"),
    #
    path('pcat/list/<str:pk>/<str:pk2>/', views.rdivPCatList, name="r-div-pcat-list"),
    path('pcat/year/list/<str:pk>/<str:pk2>/<str:year>/', views.rdivPCatYearList, name="r-div-pcat-year-list"),
    path('pcap/list/<str:pk>/<str:pk2>/', views.rdivPCapList, name="r-div-pcap-list"),
    path('pcap/year/list/<str:pk>/<str:pk2>/<str:year>/', views.rdivPCapYearList, name="r-div-pcap-year-list"),
    path('psec/list/<str:pk>/<str:pk2>/', views.rdivPSecList, name="r-div-psec-list"),
    path('psec/year/list/<str:pk>/<str:pk2>/<str:year>/', views.rdivPSecYearList, name="r-div-psec-year-list"),
    #
    path('proj/mun/summary/<str:pk>/', views.rdivPMunSum, name="r-div-proj-mun-sum"),
    path('proj/mun/list/<str:pk>/<str:pk2>/', views.rdivPMunList, name="r-div-proj-mun-list"),
    path('proj/mun/year/<str:pk>/<str:pk2>/<str:year>/', views.rdivPMunYearList, name="r-div-proj-mun-year"),
    #
    path('proj/type/summary/<str:pk>/', views.rdivPTypeSum, name="r-div-proj-type-sum"),
    path('proj/type/list/<str:pk>/<str:pk2>/', views.rdivPTypeList, name="r-div-proj-type-list"),
    path('proj/type/year/<str:pk>/<str:pk2>/<str:year>/', views.rdivPTypeYearList, name="r-div-proj-type-year"),
    # ### COMP
    path('comp/proj/sum/<str:pk>/', views.rdivCompProjSum, name="r-div-comp-proj-sum"),
    path('comp/proj/list/<str:pk>/<str:pk2>/', views.rdivCompProjList, name="r-div-comp-proj-list"),
    path('comp/proj/status/list/<str:pk>/<str:pk2>/<str:pk3>/', views.rdivCompProjStatusList, name="r-div-comp-proj-status-list"),
    path('comp/proj/year/list/<str:pk>/<str:pk2>/<str:year>/', views.rdivCompProjYearList, name="r-div-comp-proj-year-list"),
    path('comp/search/<str:pk>/', views.rdivCompSearch, name="r-div-comp-search"),
    path('cont/limit/list/<str:pk>/', views.rdivContLimitList, name="r-div-cont-limit-list"),
    # ### RAW DATA
    path('raw/data/<str:pk>/', views.rdivRawData, name="r-div-raw-data"),
    path('raw/data/cpv/<str:pk>/<str:hashid>/', views.rdivRawDataCPV, name="r-div-raw-data-cpv"),
    path('raw/data/prt/<str:pk>/<str:hashid>/', views.rdivRawDataPRT, name="r-div-raw-data-prt"),
    path('raw/data/recom/<str:pk>/<str:hashid>/', views.rdivRawDataRecom, name="r-div-raw-data-recom"),
    path('raw/data/tpo/<str:pk>/<str:hashid>/', views.rdivRawDataTPO, name="r-div-raw-data-tpo"),
    ### dg
    path('dg/', views.rdgDash, name="r-dg"),
]