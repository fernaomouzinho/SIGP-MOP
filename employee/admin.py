from django.contrib import admin
from .models import *

admin.site.register(Employee)
admin.site.register(EmployeePos)
admin.site.register(EmployeeDiv)
class EmployeeUserAdmin(admin.ModelAdmin):
	
	def has_add_permission(self, request, obj=None):
		return False
	def has_delete_permission(self, request, obj=None):
		return False
	def has_change_permission(self, request, obj=None):
		return False
	
	list_display = ('employee','user')

admin.site.register(EmployeeUser, EmployeeUserAdmin)