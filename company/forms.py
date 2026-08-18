from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.db.models import Q
from custom.models import Municipality
from .models import Company

class DateInput(forms.DateInput):
	input_type = 'date'

class CompanyForm(forms.ModelForm):
	start_date = forms.DateField(label="Data Hari", widget=DateInput(), required=False)
	class Meta:
		model = Company
		fields = ['name','reg_number','start_date','email','phone','website','address','type','country',\
			'city','municipality','lat','lng']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('name', css_class='form-group col-md-6 mb-0'),
				Column('reg_number', css_class='form-group col-md-3 mb-0'),
				Column('start_date', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('email', css_class='form-group col-md-4 mb-0'),
				Column('phone', css_class='form-group col-md-3 mb-0'),
				Column('website', css_class='form-group col-md-5 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('address', css_class='form-group col-md-6 mb-0'),
				Column('type', css_class='form-group col-md-3 mb-0'),
				Column('country', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('city', css_class='form-group col-md-3 mb-0'),
				Column('municipality', css_class='form-group col-md-3 mb-0'),
				Column('lat', css_class='form-group col-md-3 mb-0'),
				Column('lng', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Save">Save <i class="fa fa-save"></i></button> """)
		)

class uCompanyForm(forms.ModelForm):
	start_date = forms.DateField(label="Data Hari", widget=DateInput(), required=False)
	email = forms.EmailField(required=False)
	class Meta:
		model = Company
		fields = ['name','reg_number','start_date','email','phone','website','address','type','country',\
			'city','municipality']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['municipality'].queryset = Municipality.objects.exclude((Q(id=14)|Q(id=15))).all()
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('name', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('reg_number', css_class='form-group col-md-6 mb-0'),
				Column('start_date', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('email', css_class='form-group col-md-6 mb-0'),
				Column('phone', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('website', css_class='form-group col-md-6 mb-0'),
				Column('address', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('type', css_class='form-group col-md-6 mb-0'),
				Column('country', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('municipality', css_class='form-group col-md-6 mb-0'),
				Column('city', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Save">Save <i class="fa fa-save"></i></button> """)
		)