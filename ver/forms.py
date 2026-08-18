from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML
from django.db.models import Q
from django_summernote.widgets import SummernoteWidget
from django.forms import CheckboxSelectMultiple
from employee.models import Employee, EmployeePos
from ver.models import Ver, VerSecEng

class DateInput(forms.DateInput):
    input_type = 'date'

##
class VerForm(forms.ModelForm):
    start_date = forms.DateField(label="Data Hahu", widget=DateInput(), required=True)
    end_date = forms.DateField(label="Data Ikus", widget=DateInput(), required=True)
    class Meta:
        model = Ver
        fields = ['sec','epos','number','subject','start_date','end_date','file']
        widgets = {
            'number': forms.TextInput(attrs={'placeholder': 'Prense numereu ho dijitu 4, Exemplu: 0000'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['epos'].queryset = EmployeePos.objects.filter(position__id=7, cat='Verifikasaun').all()
       
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('sec', css_class='form-group col-md-12 mb-0'),
                Column('epos', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('number', css_class='form-group col-md-4 mb-0'),
                Column('start_date', css_class='form-group col-md-4 mb-0'),
                Column('end_date', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('subject', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('file', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )
        
    

class VerForm2(forms.ModelForm):
    comments = forms.CharField(label="Komentariu", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
    class Meta:
        model = Ver
        fields = ['comments']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('comments', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )

class VerForm3(forms.ModelForm):
    back_comment = forms.CharField(label="Komentariu Fila", required=False)
    class Meta:
        model = Ver
        fields = ['back_comment']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('back_comment', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            HTML(""" <button class="btn btn-secondary" type="submit" title="Rai"><i class="fa fa-reply"></i> Rai & Manda Fila</button> """)
        )
#
class VerSecForm(forms.ModelForm):
    date = forms.DateField(label="Data", widget=DateInput(), required=False)
    desc = forms.CharField(label="Deskrisaun", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
    to = forms.ModelMultipleChoiceField(
        queryset=Employee.objects.none(),  
        widget=CheckboxSelectMultiple,  
        required=False,
        label="To"
    )
 
    class Meta:
        model = VerSecEng
        fields = ['to','subject','date','desc','file']
    def __init__(self, sec, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['to'].queryset = Employee.objects.filter(employeepos__position_id=8, employeepos__cat='Verifikasaun', employeediv__sec=sec)\
                                .prefetch_related('employeepos','employeediv').all()
        # Debugging the queryset
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('to', css_class='form-group col-md-2 mb-0'),
                Column('date', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('subject', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('desc', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('file', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )

class VerSecForm2(forms.ModelForm):
    sec_comments = forms.CharField(label="Komentariu", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
    class Meta:
        model = VerSecEng
        fields = ['sec_comments','file3']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('sec_comments', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('file3', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )
#
class VerEngForm(forms.ModelForm):
    eng_comments = forms.CharField(label="Komentariu", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
    class Meta:
        model = VerSecEng
        fields = ['eng_comments','status','file2']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
             Row(
                Column('status', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('eng_comments', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('file2', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )
###