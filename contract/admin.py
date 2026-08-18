from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from .resources import ContractAdminResource




    

class ContractAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	search_fields = ['project']
	list_display = ['project']	
admin.site.register(Contract, ContractAdmin)

class ContractYearAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	search_fields = ['contract']
	list_display = ['contract']	
admin.site.register(ContractYear, ContractYearAdmin)

class ContractCompAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	search_fields = ['contract']
	list_display = ['contract']	
admin.site.register(ContractComp, ContractCompAdmin)

admin.site.register(ContractFiles)

class AmendmentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	search_fields = ['contract']
	list_display = ['contract']	
admin.site.register(Amendment, AmendmentAdmin)

admin.site.register(AmendmentPeriod)
admin.site.register(AmendmentAmount)
admin.site.register(Deduction)
admin.site.register(ContPay)