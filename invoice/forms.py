from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML
from django.db.models import Q
from django_summernote.widgets import SummernoteWidget
from invoice.models import Invoice, CertPay, PayRecom, InvLet, LetTo, InvLetAdnBack

class DateInput(forms.DateInput):
	input_type = 'date'

class InvForm(forms.ModelForm):
	date = forms.DateField(label="Data", widget=DateInput(), required=True)
	class Meta:
		model = Invoice
		fields = ['number','date','phys_prog','total','desc','file']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('number', css_class='form-group col-md-3 mb-0'),
				Column('date', css_class='form-group col-md-3 mb-0'),
				Column('phys_prog', css_class='form-group col-md-2 mb-0'),
				Column('total', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('file', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
            Row(
				Column('desc', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class CertPayForm(forms.ModelForm):
	date = forms.DateField(label="Data", widget=DateInput(), required=True)
	class Meta:
		model = CertPay
		fields = ['number','number_req','date','phys_prog','total','desc','file']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('number', css_class='form-group col-md-2 mb-0'),
    			Column('number_req', css_class='form-group col-md-2 mb-0'),
				Column('date', css_class='form-group col-md-3 mb-0'),
				Column('phys_prog', css_class='form-group col-md-2 mb-0'),
				Column('total', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('file', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('desc', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class PayRecomForm(forms.ModelForm):
	date = forms.DateField(label="Data", widget=DateInput(), required=True)
	class Meta:
		model = PayRecom
		fields = ['term','number','date','phys_prog','amount','file','desc']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('term', css_class='form-group col-md-2 mb-0'),
				Column('number', css_class='form-group col-md-2 mb-0'),
				Column('date', css_class='form-group col-md-4 mb-0'),
				Column('phys_prog', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('amount', css_class='form-group col-md-3 mb-0'),
				Column('file', css_class='form-group col-md-9 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('desc', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
###
class InvLetForm(forms.ModelForm):
	date = forms.DateField(label="Data", widget=DateInput(), required=True)
	desc = forms.CharField(label="Deskrisaun", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '250px'}}))
	class Meta:
		model = InvLet
		fields = ['number','subject','date','to','file','desc']
	def __init__(self, group, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if group == "sup": self.fields['to'].queryset = LetTo.objects.filter(id=4).all()
		elif group == "uvip": self.fields['to'].queryset = LetTo.objects.filter((Q(id=5)|Q(id=6))).all()
		elif group == "gab": self.fields['to'].queryset = LetTo.objects.filter((Q(id=3)|Q(id=7))).all()
		elif group == "dgaf": self.fields['to'].queryset = LetTo.objects.filter((Q(id=1))).all()
		elif group == "dna": self.fields['to'].queryset = LetTo.objects.filter((Q(id=2))).all()
		elif group == "dnof": self.fields['to'].queryset = LetTo.objects.filter((Q(id=8))).all()
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('number', css_class='form-group col-md-3 mb-0'),
				Column('date', css_class='form-group col-md-3 mb-0'),
				Column('subject', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
            Row(
				Column('to', css_class='form-group col-md-3 mb-0'),
				Column('file', css_class='form-group col-md-9 mb-0'),
				css_class='form-row'
			),
            Row(
				Column('desc', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
  

class InvLetForm2(forms.ModelForm):
	comment = forms.CharField(label="Komentariu", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '250px'}}))
	class Meta:
		model = InvLet
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
			HTML(""" <button class="btn btn-secondary" type="submit" title="Rai"><i class="fa fa-reply"></i> Rai & Manda Fila </button> """)
		)


class InvLetForm3(forms.ModelForm):
	date = forms.DateField(label="Data", widget=DateInput(), required=True)
	comment = forms.CharField(label="Deskrisaun", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '250px'}}))
	class Meta:
		model = InvLetAdnBack
		fields = ['number','subject','date','file','comment']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('number', css_class='form-group col-md-3 mb-0'),
				Column('date', css_class='form-group col-md-3 mb-0'),
				Column('subject', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
            Row(
				Column('file', css_class='form-group col-md-9 mb-0'),
				css_class='form-row'
			),
            Row(
				Column('comment', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)
  