from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.db.models import Q
from .models import Employee, EmployeePos, EmployeeDiv

class DateInput(forms.DateInput):
	input_type = 'date'

class EmpForm(forms.ModelForm):
	dob = forms.DateField(widget=DateInput(), required=False)
	class Meta:
		model = Employee
		fields = ['name','sex','email','phone']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('name', css_class='form-group col-md-4 mb-0'),
				Column('sex', css_class='form-group col-md-2 mb-0'),
				Column('email', css_class='form-group col-md-3 mb-0'),
				Column('phone', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Save">Save <i class="fa fa-save"></i></button> """)
		)

class EmpDivForm(forms.ModelForm):
	class Meta:
		model = EmployeeDiv
		fields = ['dg','div','dep','sec','mun']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('dg', css_class='form-group col-md-4 mb-0'),
				Column('div', css_class='form-group col-md-4 mb-0'),
				Column('dep', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('sec', css_class='form-group col-md-4 mb-0'),
				Column('mun', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Save">Save <i class="fa fa-save"></i></button> """)
		)

class EmpPosForm(forms.ModelForm):
	class Meta:
		model = EmployeePos
		fields = ['position', 'cat']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('position', css_class='form-group col-md-4 mb-0'),
    			Column('cat', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Save">Save <i class="fa fa-save"></i></button> """)
		)