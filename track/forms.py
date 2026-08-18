from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML
from django.db.models import Q
from .models import CPVReqJustify, CPVJustify, POJustify,\
	EvalJustify, ProcJustify, InvJustify, VerJustify, VerJustify2, InspJustify, InspJustify2
from django_summernote.widgets import SummernoteWidget

class DateInput(forms.DateInput):
	input_type = 'date'

class CPVReqJustifyForm(forms.ModelForm):
	comment = forms.CharField(label="Justifikasaun", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}))
	class Meta:
		model = CPVReqJustify
		fields = ['comment']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('comment', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Save">Save <i class="fa fa-save"></i></button> """)
		)

class CPVJustifyForm(forms.ModelForm):
	comment = forms.CharField(label="Justifikasaun", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}))
	class Meta:
		model = CPVJustify
		fields = ['comment']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('comment', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Save">Save <i class="fa fa-save"></i></button> """)
		)

class POJustifyForm(forms.ModelForm):
	comment = forms.CharField(label="Justifikasaun", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}))
	class Meta:
		model = POJustify
		fields = ['comment']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('comment', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Save">Save <i class="fa fa-save"></i></button> """)
		)

class EvalJustifyForm(forms.ModelForm):
	comment = forms.CharField(label="Justifikasaun", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}))
	class Meta:
		model = EvalJustify
		fields = ['comment']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('comment', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Save">Save <i class="fa fa-save"></i></button> """)
		)

class ProcJustifyForm(forms.ModelForm):
	comment = forms.CharField(label="Justifikasaun", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}))
	class Meta:
		model = ProcJustify
		fields = ['comment']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('comment', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Save">Save <i class="fa fa-save"></i></button> """)
		)

class InvJustifyForm(forms.ModelForm):
	comment = forms.CharField(label="Justifikasaun", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}))
	class Meta:
		model = InvJustify
		fields = ['comment']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('comment', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Save">Save <i class="fa fa-save"></i></button> """)
		)

class VerJustifyForm(forms.ModelForm):
	comment = forms.CharField(label="Justifikasaun", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}))
	class Meta:
		model = VerJustify
		fields = ['comment']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('comment', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Save">Save <i class="fa fa-save"></i></button> """)
		)

class VerJustify2Form(forms.ModelForm):
	comment = forms.CharField(label="Justifikasaun", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}))
	class Meta:
		model = VerJustify2
		fields = ['comment']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('comment', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Save">Save <i class="fa fa-save"></i></button> """)
		)


class InspJustifyForm(forms.ModelForm):
	comment = forms.CharField(label="Justifikasaun", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}))
	class Meta:
		model = InspJustify
		fields = ['comment']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('comment', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Save">Save <i class="fa fa-save"></i></button> """)
		)

class InspJustify2Form(forms.ModelForm):
	comment = forms.CharField(label="Justifikasaun", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}))
	class Meta:
		model = InspJustify2
		fields = ['comment']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('comment', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Save">Save <i class="fa fa-save"></i></button> """)
		)
