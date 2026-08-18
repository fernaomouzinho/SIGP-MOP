from django.urls import path
from . import views

urlpatterns = [
    path('', views.rdivHome, name="r-div-home"),
    path('ann/', views.rdivAnnHome, name="r-div-ann-home"),
    path('dash/<str:pk>/', views.rdivPayDash, name="r-div-pay-dash"),
    path('year/<str:pk>/<str:year>/', views.rdivPayYear, name="r-div-pay-year"),
    #
    path('g/dash/<str:pk>/', views.rdivPayGDash, name="r-div-pay-g-dash"),
    path('g/year/<str:pk>/<str:year>/', views.rdivPayGYear, name="r-div-pay-g-year"),
    # cat
    path('g/cat/all/<str:pk>/<str:pk2>/<str:page>/', views.rdivPayGCatAll, name="r-div-pay-g-cat-all"),
    path('g/cat/year/<str:pk>/<str:year>/<str:pk2>/<str:page>/', views.rdivPayGCatYear, name="r-div-pay-g-cat-year"),
    path('g/cat/sum/<str:pk>/', views.rdivPayGCatSum, name="r-div-pay-g-cat-sum"),
    path('g/cat/sum/year/<str:pk>/<str:year>/', views.rdivPayGCatSumYear, name="r-div-pay-g-cat-sum-year"),
    path('g/cat/sum/year/det/<str:pk>/<str:year>/<str:pk2>/', views.rdivPayGCatSumYearDet, name="r-div-pay-g-cat-sum-year-det"),
    path('g/cat/sum/month/<str:pk>/<str:year>/<str:month>/', views.rdivPayGCatSumMonth, name="r-div-pay-g-cat-sum-month"),
    path('g/cat/sum/month/det/<str:pk>/<str:year>/<str:month>/<str:pk2>/', views.rdivPayGCatSumMonthDet, name="r-div-pay-g-cat-sum-month-det"),
    # sec
    path('g/sec/all/<str:pk>/<str:pk2>/<str:page>/', views.rdivPayGSecAll, name="r-div-pay-g-sec-all"),
    path('g/sec/year/<str:year>/<str:pk>/<str:pk2>/<str:page>/', views.rdivPayGSecYear, name="r-div-pay-g-sec-year"),
    path('g/sec/sum/<str:pk>/', views.rdivPayGSecSum, name="r-div-pay-g-sec-sum"),
    path('g/sec/sum/year/<str:pk>/<str:year>/', views.rdivPayGSecSumYear, name="r-div-pay-g-sec-sum-year"),
    path('g/sec/sum/year/det/<str:pk>/<str:year>/<str:pk2>/', views.rdivPayGSecSumYearDet, name="r-div-pay-g-sec-sum-year-det"),
    path('g/sec/sum/month/<str:pk>/<str:year>/<str:month>/', views.rdivPayGSecSumMonth, name="r-div-pay-g-sec-sum-month"),
    path('g/sec/sum/month/det/<str:pk>/<str:year>/<str:month>/<str:pk2>/', views.rdivPayGSecSumMonthDet, name="r-div-pay-g-sec-sum-month-det"),
    # cap
    path('g/cap/all/<str:pk>/<str:pk2>/<str:page>/', views.rdivPayGCapAll, name="r-div-pay-g-cap-all"),
    path('g/cap/year/<str:pk>/<str:year>/<str:pk2>/<str:page>/', views.rdivPayGCapYear, name="r-div-pay-g-cap-year"),
    path('g/cap/sum/<str:pk>/', views.rdivPayGCapSum, name="r-div-pay-g-cap-sum"),
    path('g/cap/sum/year/<str:pk>/<str:year>/', views.rdivPayGCapSumYear, name="r-div-pay-g-cap-sum-year"),
    path('g/cap/sum/year/det/<str:pk>/<str:year>/<str:pk2>/', views.rdivPayGCapSumYearDet, name="r-div-pay-g-cap-sum-year-det"),
    path('g/cap/sum/month/<str:pk>/<str:year>/<str:month>/', views.rdivPayGCapSumMonth, name="r-div-pay-g-cap-sum-month"),
    path('g/cap/sum/month/det/<str:pk>/<str:year>/<str:month>/<str:pk2>/', views.rdivPayGCapSumMonthDet, name="r-div-pay-g-cap-sum-month-det"),
    #
    path('year/list/<str:pk>/<str:year>/<str:page>/', views.rdivPayYearList, name="r-div-pay-year-list"),
    path('month/list/<str:pk>/<str:year>/<str:month>/<str:page>/', views.rdivPayMonthList, name="r-div-pay-month-list"),
    path('date/list/<str:pk>/<str:year>/<str:month>/<str:date>/<str:page>/', views.rdivPayDateList, name="r-div-pay-date-list"),
    ### FISCAL
    path('fis/dash/<str:pk>/', views.rdivPayFisDash, name="r-div-pay-fis-dash"),
    path('fis/year/<str:pk>/<str:year>/', views.rdivPayFisYear, name="r-div-pay-fis-year"),
    # cat
    path('fis/cat/all/<str:pk>/<str:pk2>/<str:page>/', views.rdivPayFisCatAll, name="r-div-pay-fis-cat-all"),
    path('fis/cat/year/<str:pk>/<str:year>/<str:pk2>/<str:page>/', views.rdivPayFisCatYear, name="r-div-pay-fis-cat-year"),
    path('fis/cat/sum/<str:pk>/', views.rdivPayFisCatSum, name="r-div-pay-fis-cat-sum"),
    path('fis/cat/sum/year/<str:pk>/<str:year>/', views.rdivPayFisCatSumYear, name="r-div-pay-fis-cat-sum-year"),
    path('fis/cat/sum/year/det/<str:pk>/<str:year>/<str:pk2>/', views.rdivPayFisCatSumYearDet, name="r-div-pay-fis-cat-sum-year-det"),
    path('fis/cat/sum/month/<str:pk>/<str:year>/<str:month>/', views.rdivPayFisCatSumMonth, name="r-div-pay-fis-cat-sum-month"),
    path('fis/cat/sum/month/det/<str:pk>/<str:year>/<str:month>/<str:pk2>/', views.rdivPayFisCatSumMonthDet, name="r-div-pay-fis-cat-sum-month-det"),
    # sec
    path('fis/sec/all/<str:pk>/<str:pk2>/<str:page>/', views.rdivPayFisSecAll, name="r-div-pay-fis-sec-all"),
    path('fis/sec/year/<str:pk>/<str:year>/<str:pk2>/<str:page>/', views.rdivPayFisSecYear, name="r-div-pay-fis-sec-year"),
    path('fis/sec/sum/<str:pk>/', views.rdivPayFisSecSum, name="r-div-pay-fis-sec-sum"),
    path('fis/sec/sum/year/<str:pk>/<str:year>/', views.rdivPayFisSecSumYear, name="r-div-pay-fis-sec-sum-year"),
    path('fis/sec/sum/year/det/<str:pk>/<str:year>/<str:pk2>/', views.rdivPayFisSecSumYearDet, name="r-div-pay-fis-sec-sum-year-det"),
    path('fis/sec/sum/month/<str:pk>/<str:year>/<str:month>/', views.rdivPayFisSecSumMonth, name="r-div-pay-fis-sec-sum-month"),
    path('fis/sec/sum/month/det/<str:pk>/<str:year>/<str:month>/<str:pk2>/', views.rdivPayFisSecSumMonthDet, name="r-div-pay-fis-sec-sum-month-det"),
    # cap
    path('fis/cap/all/<str:pk>/<str:pk2>/<str:page>/', views.rdivPayFisCapAll, name="r-div-pay-fis-cap-all"),
    path('fis/cap/year/<str:pk>/<str:year>/<str:pk2>/<str:page>/', views.rdivPayFisCapYear, name="r-div-pay-fis-cap-year"),
    path('fis/cap/sum/<str:pk>/', views.rdivPayFisCapSum, name="r-div-pay-fis-cap-sum"),
    path('fis/cap/sum/year/<str:pk>/<str:year>/', views.rdivPayFisCapSumYear, name="r-div-pay-fis-cap-sum-year"),
    path('fis/cap/sum/year/det/<str:pk>/<str:year>/<str:pk2>/', views.rdivPayFisCapSumYearDet, name="r-div-pay-fis-cap-sum-year-det"),
    path('fis/cap/sum/month/<str:pk>/<str:year>/<str:month>/', views.rdivPayFisCapSumMonth, name="r-div-pay-fis-cap-sum-month"),
    path('fis/cap/sum/month/det/<str:pk>/<str:year>/<str:month>/<str:pk2>/', views.rdivPayFisCapSumMonthDet, name="r-div-pay-fis-cap-sum-month-det"),
    ### ANNUAL
    path('ann/dash/<str:pk>/', views.rdivPayAnnDash, name="r-div-pay-ann-dash"),
    path('ann/year/<str:pk>/<str:year>/', views.rdivPayAnnYear, name="r-div-pay-ann-year"),
    # cat
    path('ann/cat/all/<str:pk>/<str:pk2>/<str:page>/', views.rdivPayAnnCatAll, name="r-div-pay-ann-cat-all"),
    path('ann/cat/year/<str:pk>/<str:year>/<str:pk2>/<str:page>/', views.rdivPayAnnCatYear, name="r-div-pay-ann-cat-year"),
    path('ann/cat/sum/<str:pk>/', views.rdivPayAnnCatSum, name="r-div-pay-ann-cat-sum"),
    path('ann/cat/sum/year/<str:pk>/<str:year>/', views.rdivPayAnnCatSumYear, name="r-div-pay-ann-cat-sum-year"),
    path('ann/cat/sum/year/det/<str:pk>/<str:year>/<str:pk2>/', views.rdivPayAnnCatSumYearDet, name="r-div-pay-ann-cat-sum-year-det"),
    path('ann/cat/sum/month/<str:pk>/<str:year>/<str:month>/', views.rdivPayAnnCatSumMonth, name="r-div-pay-ann-cat-sum-month"),
    path('ann/cat/sum/month/det/<str:pk>/<str:year>/<str:month>/<str:pk2>/', views.rdivPayAnnCatSumMonthDet, name="r-div-pay-ann-cat-sum-month-det"),
    # sec
    path('ann/sec/all/<str:pk>/<str:pk2>/<str:page>/', views.rdivPayAnnSecAll, name="r-div-pay-ann-sec-all"),
    path('ann/sec/year/<str:pk>/<str:year>/<str:pk2>/<str:page>/', views.rdivPayAnnSecYear, name="r-div-pay-ann-sec-year"),
    path('ann/sec/sum/<str:pk>/', views.rdivPayAnnSecSum, name="r-div-pay-ann-sec-sum"),
    path('ann/sec/sum/year/<str:pk>/<str:year>/', views.rdivPayAnnSecSumYear, name="r-div-pay-ann-sec-sum-year"),
    path('ann/sec/sum/year/det/<str:pk>/<str:year>/<str:pk2>/', views.rdivPayAnnSecSumYearDet, name="r-div-pay-ann-sec-sum-year-det"),
    path('ann/sec/sum/month/<str:pk>/<str:year>/<str:month>/', views.rdivPayAnnSecSumMonth, name="r-div-pay-ann-sec-sum-month"),
    path('ann/sec/sum/month/det/<str:pk>/<str:year>/<str:month>/<str:pk2>/', views.rdivPayAnnSecSumMonthDet, name="r-div-pay-ann-sec-sum-month-det"),
    # cap
    path('ann/cap/all/<str:pk>/<str:pk2>/<str:page>/', views.rdivPayAnnCapAll, name="r-div-pay-ann-cap-all"),
    path('ann/cap/year/<str:pk>/<str:year>/<str:pk2>/<str:page>/', views.rdivPayAnnCapYear, name="r-div-pay-ann-cap-year"),
    path('ann/cap/sum/<str:pk>/', views.rdivPayAnnCapSum, name="r-div-pay-ann-cap-sum"),
    path('ann/cap/sum/year/<str:pk>/<str:year>/', views.rdivPayAnnCapSumYear, name="r-div-pay-ann-cap-sum-year"),
    path('ann/cap/sum/year/det/<str:pk>/<str:year>/<str:pk2>/', views.rdivPayAnnCapSumYearDet, name="r-div-pay-ann-cap-sum-year-det"),
    path('ann/cap/sum/month/<str:pk>/<str:year>/<str:month>/', views.rdivPayAnnCapSumMonth, name="r-div-pay-ann-cap-sum-month"),
    path('ann/cap/sum/month/det/<str:pk>/<str:year>/<str:month>/<str:pk2>/', views.rdivPayAnnCapSumMonthDet, name="r-div-pay-ann-cap-sum-month-det"),
    ### EXEC
    path('exec/list/<str:pk>/', views.rdivExecList, name="r-div-exec-list"),
    path('exec/<str:pk>/<str:year>/', views.rdivExecYearList, name="r-div-exec-year-list"),
    path('exec/pay/all/<str:pk>/<str:month>/', views.rdivExecPayAllList, name="r-div-exec-pay-all-list"),
    path('exec/pay/year/<str:pk>/<str:year>/<str:month>/', views.rdivExecPayYearList, name="r-div-exec-pay-year-list"),
    ### dg
    path('dg/', views.rdgHome, name="r-dg-home"),
    path('dg/ann/', views.rdgAnnHome, name="r-dg-ann-home"),
]