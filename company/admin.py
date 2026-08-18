from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin



class CompanyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	search_fields = ['name']
	list_display = ['name']	
admin.site.register(Company, CompanyAdmin)

class CompUserAdmin(admin.ModelAdmin):
	def has_add_permission(self, request, obj=None):
		return False
	def has_delete_permission(self, request, obj=None):
		return False
	def has_change_permission(self, request, obj=None):
		return False
admin.site.register(CompUser, CompUserAdmin)