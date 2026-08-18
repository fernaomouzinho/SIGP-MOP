from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

class AdministrativePostAdmin(admin.ModelAdmin):
    search_fields = ['name', 'municipality__name']
class VillageAdmin(admin.ModelAdmin):
    search_fields = ['name', 'administrativepost__name', 'administrativepost__municipality__name']
class AldeiaAdmin(admin.ModelAdmin):
    search_fields = ['name', 'village__name']

admin.site.register(Year)
admin.site.register(FiscalYear)
admin.site.register(Fund)
admin.site.register(Capital)
admin.site.register(PType)
admin.site.register(PTypes)
admin.site.register(PCategory)
admin.site.register(PCat)
admin.site.register(Owner)
admin.site.register(CType) #contract type
admin.site.register(Book)
admin.site.register(Sector)
admin.site.register(StatusProj)
admin.site.register(StatusPlan)
admin.site.register(Program)

class StatusImpAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	search_fields = ['name']
	list_display = ['name']	
admin.site.register(StatusImp, StatusImpAdmin)


admin.site.register(Country)
admin.site.register(Position)


class MunicipalityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	search_fields = ['name']
	list_display = ['name']	
admin.site.register(Municipality, MunicipalityAdmin)

admin.site.register(AdministrativePost, AdministrativePostAdmin)
admin.site.register(Village, VillageAdmin)
admin.site.register(Aldeia, AldeiaAdmin)
#
admin.site.register(Ministery)
admin.site.register(Min)
admin.site.register(DG)
admin.site.register(Division)
admin.site.register(Section)
admin.site.register(Department)
