from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from .resources import ProjectAdminResource



class ProjectAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ['code', 'name']
admin.site.register(Project, ProjectAdmin)
    

class ProjectLocAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	search_fields = ['project']
	list_display = ['project']	
admin.site.register(ProjectLoc, ProjectLocAdmin)


class ProjectEstAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	search_fields = ['project']
	list_display = ['project']	
admin.site.register(ProjectEst, ProjectEstAdmin)


