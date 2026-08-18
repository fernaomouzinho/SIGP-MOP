from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.db.models import Q
from django_summernote.widgets import SummernoteWidget
from payment.models import Payment, PhysicalProgress,PaymentPortal

class DateInput(forms.DateInput):
	input_type = 'date'

class PayForm(forms.ModelForm):
	class Meta:
		model = Payment
		fields = ['desc']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('desc', css_class='form-group col-md-9 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Save">Save <i class="fa fa-save"></i></button> """)
		)
###
class customPayForm(forms.ModelForm):
	date = forms.DateField(label="Data", widget=DateInput(), required=False)
	class Meta:
		model = Payment
		fields = ['phys_prog','total','date','desc']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('phys_prog', css_class='form-group col-md-4 mb-0'),
				Column('date', css_class='form-group col-md-4 mb-0'),
				Column('total', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('desc', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Save">Save <i class="fa fa-save"></i></button> """)
		)

class customPayForm2(forms.ModelForm):
	date = forms.DateField(label="Data", widget=DateInput(), required=False)
	class Meta:
		model = Payment
		fields = ['phys_prog','date','desc']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('phys_prog', css_class='form-group col-md-3 mb-0'),
				Column('date', css_class='form-group col-md-3 mb-0'),
				Column('desc', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Save">Save <i class="fa fa-save"></i></button> """)
		)
  
class physicalProgressForm(forms.ModelForm):
	date = forms.DateField(label="Data", widget=DateInput(), required=False)
	class Meta:
		model = PhysicalProgress
		fields = ['prog_percent','date']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('prog_percent', css_class='form-group col-md-3 mb-0'),
				Column('date', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Save">Save <i class="fa fa-save"></i></button> """)
		)
  
  
class PaymentPortalForm(forms.ModelForm):
    datetime = forms.DateTimeField(
        label="Date & Time",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False
    )

    class Meta:
        model = PaymentPortal
        fields = ['pcategory', 'amount', 'percent', 'year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('pcategory', css_class='form-group col-md-4 mb-0'),
                Column('amount', css_class='form-group col-md-3 mb-0'),
                Column('percent', css_class='form-group col-md-3 mb-0'),
                  Column('year', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
           
            HTML(""" 
                <button class="btn btn-primary" type="submit" title="Save">
                    Save <i class="fa fa-save"></i>
                </button> 
            """)
        )