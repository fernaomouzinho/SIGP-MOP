from import_export import resources, fields
from .models import Contract
from import_export.widgets import ForeignKeyWidget
from custom.models import *
from project.models import *


class ContractAdminResource(resources.ModelResource):
    
    project = fields.Field(column_name='project', attribute='project', widget=ForeignKeyWidget(Project, field='name'))
    status = fields.Field(column_name='status', attribute='status', widget=ForeignKeyWidget(StatusImp, field='name'))
    type = fields.Field(column_name='type', attribute='type', widget=ForeignKeyWidget(CType, field='name'))
    
    class Meta:

        model = Contract
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ['id']
        fields = ('id',
            'project__code', 
            'project', 
            'project__capital__name',
            'status',
            'type',
            'number',
            'total',
            'start_date',
            'end_date',
            'proc_year',
            'company_type',
            'desc',
            'is_fiscal',
            'is_active',
            'is_lock',
            'is_ready',
            'is_complete',
            'is_stop',
            'stop_date',
            'stop_comment',
            'datetime',
            'user',
            'hashed',  
        )
        
        export_order = ('id',
            'project__code',             
            'project',           
            'project__capital__name',
            'status',
            'type',
            'number',
            'total',
            'start_date',
            'end_date',
            'proc_year',
            'company_type',
            'desc',
            'is_fiscal',
            'is_active',
            'is_lock',
            'is_ready',
            'is_complete',
            'is_stop',
            'stop_date',
            'stop_comment',
            'datetime',
            'user',
            'hashed', )


