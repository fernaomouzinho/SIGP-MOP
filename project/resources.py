from import_export import resources, fields
from .models import Project
from import_export.widgets import ForeignKeyWidget
from custom.models import *


class ProjectAdminResource(resources.ModelResource):
    
    owner_name = fields.Field(column_name='owner', attribute='owner', widget=ForeignKeyWidget(Owner, field='name'))
    capital = fields.Field(column_name='capital', attribute='capital', widget=ForeignKeyWidget(Capital, field='name'))
    pcategory = fields.Field(column_name='pcategory', attribute='pcategory', widget=ForeignKeyWidget(PCategory, field='name'))
    pcat = fields.Field(column_name='pcat', attribute='pcat', widget=ForeignKeyWidget(PCat, field='name'))
    statusproj = fields.Field(column_name='statusproj', attribute='statusproj', widget=ForeignKeyWidget(StatusProj, field='name'))
    status = fields.Field(column_name='status', attribute='status', widget=ForeignKeyWidget(StatusPlan, field='name'))
    sector = fields.Field(column_name='sector', attribute='sector', widget=ForeignKeyWidget(Sector, field='name'))
    ptype = fields.Field(column_name='ptype', attribute='ptype', widget=ForeignKeyWidget(PType, field='id'))
    ptypes = fields.Field(column_name='ptypes', attribute='ptypes', widget=ForeignKeyWidget(PTypes, field='id'))
    fund = fields.Field(column_name='fund', attribute='fund', widget=ForeignKeyWidget(Fund, field='name'))
    book = fields.Field(column_name='book', attribute='book', widget=ForeignKeyWidget(Book, field='name'))
    year = fields.Field(column_name='year', attribute='year', widget=ForeignKeyWidget(Year, field='year'))
   
    class Meta:

        model = Project
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ['id']
        fields = ('id',
            'code',
            'name',
            'name2',
            'owner',
            'capital',
            'pcategory',
            'pcat',
            'statusproj',
            'status',
            'sector',
            'ptype',
            'ptypes',
            'fund',
            'book',
            'year',
            'alocate_bd',
            'year_alocate_bd',
            'desc',
            'is_active',
            'is_read',
            'is_lock',
            'is_ready',
            'is_eval',
            'is_cont',
            'is_adn',
            'is_end',
            'datetime',
            'user',
            'hashed',  
        )
        
        export_order = ('id',
            'code',
            'name',
            'name2',
            'owner',
            'capital',
            'pcategory',
            'pcat',
            'statusproj',
            'status',
            'sector',
            'ptype',
            'ptypes',
            'fund',
            'book',
            'year',
            'alocate_bd',
            'year_alocate_bd',
            'desc',
            'is_active',
            'is_read',
            'is_lock',
            'is_ready',
            'is_eval',
            'is_cont',
            'is_adn',
            'is_end',
            'datetime',
            'user',
            'hashed', )


