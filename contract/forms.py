from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.db.models import Q
from django_summernote.widgets import SummernoteWidget
from company.models import Company
from contract.models import Contract, ContractComp, ContractFiles, AmendmentPeriod, AmendmentAmount,\
	Deduction, ContractYear
from project.models import Project

class DateInput(forms.DateInput):
	input_type = 'date'

class ContForm(forms.ModelForm):
	start_date = forms.DateField(label="Data Hahu", widget=DateInput(), required=True)
	end_date = forms.DateField(label="Data Remata", widget=DateInput(), required=True)
	class Meta:
		model = Contract
		fields = ['project','type','number','total','start_date','end_date',\
            'company_type','desc','proc_year','is_fiscal']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['project'].queryset = Project.objects.filter(is_end=False).all().order_by('-year','-id')
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('project', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
            Row(
				Column('type', css_class='form-group col-md-3 mb-0'),
				Column('number', css_class='form-group col-md-4 mb-0'),
				Column('total', css_class='form-group col-md-3 mb-0'),
				Column('is_fiscal', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
			),
            Row(
				Column('company_type', css_class='form-group col-md-3 mb-0'),
				Column('start_date', css_class='form-group col-md-3 mb-0'),
				Column('end_date', css_class='form-group col-md-3 mb-0'),
				Column('proc_year', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
            Row(
				Column('desc', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class ContStatusForm(forms.ModelForm):
	class Meta:
		model = Contract
		fields = ['status']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('status', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class ContStopForm(forms.ModelForm):
	stop_date = forms.DateField(label="Data Remata", widget=DateInput(), required=True)
	stop_comment = forms.CharField(label="Rajaun Hapara Kontratu", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	class Meta:
		model = Contract
		fields = ['is_stop','stop_date','stop_comment']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('is_stop', css_class='form-group col-md-3 mb-0'),
				Column('stop_date', css_class='form-group col-md-3 mb-0'),
				Column('stop_comment', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class ContCompForm(forms.ModelForm):
	class Meta:
		model = ContractComp
		fields = ['company','is_main']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['company'].queryset = Company.objects.all().order_by('name')
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('company', css_class='form-group col-md-10 mb-0'),
				Column('is_main', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class ContFilesForm(forms.ModelForm):
	class Meta:
		model = ContractFiles
		fields = ['desc','file']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('desc', css_class='form-group col-md-6 mb-0'),
                Column('file', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
###
class AmendPeriodForm(forms.ModelForm):
	end_date = forms.DateField(label="Data Extende", widget=DateInput(), required=True)
	class Meta:
		model = AmendmentPeriod
		fields = ['number','end_date','desc']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('number', css_class='form-group col-md-3 mb-0'),
				Column('end_date', css_class='form-group col-md-3 mb-0'),
				Column('desc', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class AmendAmountForm(forms.ModelForm):
	class Meta:
		model = AmendmentAmount
		fields = ['number','total','desc']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('number', css_class='form-group col-md-3 mb-0'),
				Column('total', css_class='form-group col-md-3 mb-0'),
				Column('desc', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class DeductionForm(forms.ModelForm):
	class Meta:
		model = Deduction
		fields = ['total','desc']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('total', css_class='form-group col-md-4 mb-0'),
				Column('desc', css_class='form-group col-md-8 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
##
class ContractYearForm(forms.ModelForm):
	class Meta:
		model = ContractYear
		fields = ['total','year']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('total', css_class='form-group col-md-3 mb-0'),
				Column('year', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
##
