from django.urls import path
from . import views

urlpatterns = [
    path('uvip/list/', views.uvipProjList, name="uvip-proj-list"),
    path('uvip/detail/<str:hashid>/', views.uvipProjDetail, name="uvip-proj-det"),
    path('uvip/add/', views.uvipProjAdd, name="uvip-proj-add"),
    path('uvip/edit/<str:hashid>/', views.uvipProjEdit, name="uvip-proj-edit"),
    path('uvip/rem/<str:hashid>/', views.uvipProjRem, name="uvip-proj-rem"),
    path('uvip/lock/<str:hashid>/', views.uvipProjLock, name="uvip-proj-lock"),
    path('uvip/unlock/<str:hashid>/', views.uvipProjUnlock, name="uvip-proj-unlock"),
    path('uvip/ready/<str:hashid>/', views.uvipProjReady, name="uvip-proj-ready"),
    path('uvip/status/edit/<str:hashid>/', views.uvipProjStatusEdit, name="uvip-proj-status-edit"),
    path('uvip/est/edit/<str:hashid>/<str:pk>/', views.uvipProjEstEdit, name="uvip-proj-est-edit"),
    path('uvip/est/rem/<str:hashid>/<str:pk>/', views.uvipProjEstRem, name="uvip-proj-est-rem"),
    path('uvip/year/<str:year>/', views.uvipProjYear, name="uvip-proj-year"),
    path('uvip/adn/edit/<str:hashid>/', views.uvipProjADNEdit, name="uvip-proj-adn-edit"),
    path('op/est/edit/<str:hashid>/<str:pk>/', views.opProjEstEdit, name="op-proj-est-edit"),
    ### ALL
    path('list/', views.ProjList, name="proj-list"),
    path('detail/<str:hashid>/', views.ProjDetail, name="proj-det"),
    path('raw/data/', views.ProjRawData, name="proj-raw-data"),
    ### DIV
    path('div/detail/<str:hashid>/', views.divProjDetail, name="div-proj-det"),
    path('div/loc/edit/<str:hashid>/<str:pk>/', views.divProjLocEdit, name="div-proj-loc-edit"),
    path('div/est/edit/<str:hashid>/<str:pk>/', views.divProjEstEdit, name="div-proj-est-edit"),
    path('div/est/rem/<str:hashid>/<str:pk>/', views.divProjEstRem, name="div-proj-est-rem"),
    #
    path('year/all/', views.ProjYearAll, name="proj-year-all"),
    path('year/list/<str:year>/', views.ProjYearList, name="proj-year-list"),
    path('locs/list/', views.ProjLocList, name="proj-loc-list"),
    #
    path('uvip/custom/list/', views.uvipProjCustomList, name="uvip-proj-custom-list"),
    path('uvip/hash/update/', views.uvipProjHashUpdate, name="uvip-proj-hash-update"),
    path('uvip/imp/', views.uvipProjImport, name="uvip-proj-imp"),
    ### SUP
    path('sup/list/', views.supProjList, name="sup-proj-list"),
    path('sup/det/<str:hashid>/', views.supProjDetail, name="sup-proj-det"),
]