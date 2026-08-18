from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.db.models import Q
from custom.models import AdministrativePost, Aldeia, Village, StatusPlan, Year
from .models import Project, ProjectLoc, ProjectEst

class DateInput(forms.DateInput):
	input_type = 'date'

class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ['code','code_act','name','program','owner','capital','pcategory','pcat','sector','ptypes','fund','book','status','year','alocate_bd','year_alocate_bd','statusproj','desc']
		widgets = {
            'code': forms.TextInput(attrs={'placeholder': '0000'}),
        }
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['year'].queryset = Year.objects.filter().order_by('-year')
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('name', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('code', css_class='form-group col-md-3 mb-0'),
                Column('code_act', css_class='form-group col-md-3 mb-0'),
                Column('program', css_class='form-group col-md-3 mb-0'),
				Column('owner', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('capital', css_class='form-group col-md-4 mb-0'),
				Column('pcategory', css_class='form-group col-md-3 mb-0'),
				Column('pcat', css_class='form-group col-md-3 mb-0'),
				Column('fund', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('book', css_class='form-group col-md-3 mb-0'),
				# Column('ptype', css_class='form-group col-md-3 mb-0'),
    			Column('ptypes', css_class='form-group col-md-3 mb-0'),
				Column('sector', css_class='form-group col-md-3 mb-0'),
    			Column('status', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('year', css_class='form-group col-md-3 mb-0'),
    			Column('alocate_bd', css_class='form-group col-md-3 mb-0'),
    			Column('year_alocate_bd', css_class='form-group col-md-3 mb-0'),
				Column('statusproj', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('desc', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class ProjectStatusForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ['statusproj']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('statusproj', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class ProjectLocForm(forms.ModelForm):
	class Meta:
		model = ProjectLoc
		fields = ['municipality','administrativepost','village','aldeia',\
			'start_lat','start_lng','end_lat','end_lng']
	def __init__(self, *args, **kwargs):
		super(ProjectLocForm, self).__init__(*args, **kwargs)
		self.fields['administrativepost'].queryset = AdministrativePost.objects.none()
		self.fields['village'].queryset = Village.objects.none()
		self.fields['aldeia'].queryset = Aldeia.objects.none()
		
		if 'municipality' in self.data:
			try:
				municipality_id = int(self.data.get('municipality'))
				self.fields['administrativepost'].queryset = AdministrativePost.objects.filter(municipality_id=municipality_id).order_by('-id')
			except (ValueError, TypeError):
				pass
		elif self.instance.pk and self.instance.municipality:
			self.fields['administrativepost'].queryset = self.instance.municipality.administrativepost_set.order_by('-id')

		if 'administrativepost' in self.data:
			try:
				administrativepost_id = int(self.data.get('administrativepost'))
				self.fields['village'].queryset = Village.objects.filter(administrativepost_id=administrativepost_id).order_by('-id')
			except (ValueError, TypeError):
				pass
		elif self.instance.pk and self.instance.administrativepost:
			self.fields['village'].queryset = self.instance.administrativepost.village_set.order_by('name')

		if 'village' in self.data:
			try:
				village_id = int(self.data.get('village'))
				self.fields['aldeia'].queryset = Aldeia.objects.filter(village_id=village_id).order_by('-id')
			except (ValueError, TypeError):
				pass
		elif self.instance.pk and self.instance.village:
			self.fields['aldeia'].queryset = self.instance.village.aldeia_set.order_by('name')

class ProjectEstForm1(forms.ModelForm):
	class Meta:
		model = ProjectEst
		fields = ['owner']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('owner', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class ProjectEstForm2(forms.ModelForm):
	class Meta:
		model = ProjectEst
		fields = ['adn']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('adn', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class ProjectEstForm3(forms.ModelForm):
	class Meta:
		model = ProjectEst
		fields = ['owner','adn']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('owner', css_class='form-group col-md-3 mb-0'),
				Column('adn', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

###
class ProjADNForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ['is_adn']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('is_adn', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)