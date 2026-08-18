from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.contrib.auth.models import User

class DateInput(forms.DateInput):
	input_type = 'date'

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ['username','email']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('username', css_class='form-group col-md-6 mb-0'),
				Column('email', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-sm btn-info" type="submit">Rai <i class="fa fa-save"></i></button> """)
		)