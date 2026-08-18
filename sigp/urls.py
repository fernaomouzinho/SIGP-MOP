"""sigp URL Configuration

The `urlpn/atterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from main import views as main_views
from django.conf.urls import handler404, handler500
from django.views.static import serve
from rest_framework.authtoken.views import obtain_auth_token

admin.site.site_header = 'SIGP-MOP SUPER USER'

urlpatterns = [
    path('djadmin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),
	path('login/', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='home/logout.html'), name='logout'),
    path('api/', include('main.api.urls')),
	path('summernote/', include('django_summernote.urls')),
    path('home/', main_views.home, name='home'),
    path('custom/', include('custom.urls')),
    path('emp/', include('employee.urls')),
    path('proj/', include('project.urls')),
    path('api/proj/', include('project.api.urls')),
    path('company/', include('company.urls')),
    path('api/company/', include('company.api.urls')),
    path('api/token/', obtain_auth_token),  # POST username + password → get token
    path('fin/', include('finance.urls')),
    path('notif/', include('notif.urls')),
    path('eval/', include('eval.urls')), 
    path('proc/', include('proc.urls')),
    path('cont/', include('contract.urls')),
    path('api/cont/', include('contract.api.urls')),
    path('inv/', include('invoice.urls')), 
    path('inv/let/', include('invoice.urls_let')),
    path('api/inv/', include('invoice.api.urls')),
    path('ver/', include('ver.urls')), 
    path('insp/', include('insp.urls')), 
    path('payment/', include('payment.urls')),
    path('track/', include('track.urls')), 
    path('report/', include('report.urls')), 
    path('report/pay/', include('report.urls_pay')), 
    path('div/report/', include('reportdiv.urls')), 
    path('div/report/pay/', include('reportdiv.urls_pay')), 
    path('chart/', include('chart.urls')), 
   
    path('api/chart/', include('chart.api.urls')), 
    path('user/', include('users.urls')), 
    
    # Api Mobile
    path('api/mobile/', include('project.api_mobile.urls')),
    #    
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

handler404 = 'main.views.error_404'
handler500 = 'main.views.error_500'

# if settings.DEBUG:
	# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)