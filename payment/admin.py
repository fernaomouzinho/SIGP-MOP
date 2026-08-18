from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin


class PaymentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	search_fields = ['contract']
	list_display = ['contract']	
admin.site.register(Payment, PaymentAdmin)


admin.site.register(PaymentFiscal)
admin.site.register(PaymentHist)

class PhysicalProgressAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	search_fields = ['contract']
	list_display = ['contract']	
admin.site.register(PhysicalProgress, PhysicalProgressAdmin)

class PaymentPortalAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	search_fields = ['program','pcategory']
	list_display = ['program','pcategory','amount','year']	
	ordering = ['pcategory','program']
admin.site.register(PaymentPortal, PaymentPortalAdmin)

