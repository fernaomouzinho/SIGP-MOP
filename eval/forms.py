from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.db.models import Q
from django_summernote.widgets import SummernoteWidget
from custom.models import Division
from project.models import Project
from eval.models import Eval, EvalFile, EvalLet, LetTo, EvalLetAdnBack, EvalTrack, EvalFITrack,EvalLetCNABack

class DateInput(forms.DateInput):
    input_type = 'date'

class EvalForm(forms.ModelForm):
    date = forms.DateField(label="Data", widget=DateInput(), required=False)
    desc = forms.CharField(label="Deskrisaun", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
    class Meta:
        model = Eval
        fields = ['proj','number','date','desc']
        widgets = {
            'number': forms.TextInput(attrs={'placeholder': '0000'}),
        }
    def __init__(self, div, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proj'].queryset = Project.objects.filter(owner=div, is_cont=False).all().order_by('-year','-id')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('proj', css_class='form-group col-md-6 mb-0'),
                Column('number', css_class='form-group col-md-3 mb-0'),
                Column('date', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('desc', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )

class EvalForm2(forms.ModelForm):
    class Meta:
        model = Eval
        fields = ['is_adn','is_cna']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('is_adn', css_class='form-group col-md-2 mb-0'),
                Column('is_cna', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )
        
# Eval Return Form   
class EvalForm3(forms.ModelForm):
    return_date = forms.DateField(label="Data", widget=DateInput(), required=False)
    class Meta:
        model = Eval
        fields = ['return_comment','return_date']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('return_date', css_class='form-group col-md-2 mb-0'),
                Column('return_comment', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )
        

class EvalFileForm(forms.ModelForm):
    class Meta:
        model = EvalFile
        fields = ['file_boq','file_design','file_spec','file_mapq','file_docoth','desc']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('desc', css_class='form-group col-md-6 mb-0'),
                Column('file_boq', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
               Row(
                
                Column('file_design', css_class='form-group col-md-6 mb-0'),
                Column('file_spec', css_class='form-group col-md-6 mb-0'),
                Column('file_mapq', css_class='form-group col-md-6 mb-0'),
                Column('file_docoth', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )
        

        
        
        
        

class EvalLetForm(forms.ModelForm):
    date = forms.DateField(label="Data", widget=DateInput(), required=False)
    desc = forms.CharField(label="Deskrisaun", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
    class Meta:
        model = EvalLet
        fields = ['number','subject','date','to','desc','file']
        widgets = {
            'number': forms.TextInput(attrs={'placeholder': '0000'}),
        }
    def __init__(self, *args, **kwargs):
        eval_instance = kwargs.pop('eval', None)  # Extract passed eval
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('number', css_class='form-group col-md-4 mb-0'),
                Column('date', css_class='form-group col-md-4 mb-0'),
                Column('to', css_class='form-group col-md-4 mb-0'),
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

class EvalLetForm2(forms.ModelForm):
    comment = forms.CharField(label="Komentariu", required=True, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
    class Meta:
        model = EvalLet
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
            HTML(""" <button class="btn btn-secondary" type="submit" title="Rai & Manda Fila"><i class="fa fa-reply"></i> Rai & Manda Fila</button> """)
        )

class EvalLetForm3(forms.ModelForm):
    date = forms.DateField(label="Data", widget=DateInput(), required=False)
    comment = forms.CharField(label="Komentariu", required=True, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
    class Meta:
        model = EvalLetAdnBack
        fields = ['number','subject','date','file', 'comment']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('number', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
             Row(
                Column('subject', css_class='form-group col-md-6 mb-0'),
                Column('date', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
             Row(
                Column('comment', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('file', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            HTML(""" <button class="btn btn-secondary" type="submit" title="Rai & Manda Fila"><i class="fa fa-reply"></i> Rai & Manda Fila</button> """)
        )


class EvalLetForm4(forms.ModelForm):
    date = forms.DateField(label="Data Karta", widget=DateInput(), required=False)
    comment = forms.CharField(label="Komentariu", required=True, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
    class Meta:
        model = EvalLetAdnBack
        fields = ['number','subject','date','file','file_boq','file_design','file_spec','file_mapq', 'file_docoth','comment']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('number', css_class='form-group col-md-2 mb-0'),
                Column('subject', css_class='form-group col-md-4 mb-0'),
                Column('date', css_class='form-group col-md-3 mb-0'),
                Column('file', css_class='form-group col-md-3 mb-0'),
                
                css_class='form-row'
            ),
            Row(
                Column('comment', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('file_boq', css_class='form-group col-md-3 mb-0'),
                Column('file_design', css_class='form-group col-md-3 mb-0'),
                Column('file_spec', css_class='form-group col-md-3 mb-0'),
                Column('file_mapq', css_class='form-group col-md-3 mb-0'),
                Column('file_docoth', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            HTML(""" <button class="btn btn-secondary" type="submit" title="Rai & Manda Fila"><i class="fa fa-reply"></i> Rai & Manda Fila</button> """)
        )
        
# Eval FI Return From CNA
class EvalLetForm5(forms.ModelForm):
    date = forms.DateField(label="Data Karta", widget=DateInput(), required=False)
    comment = forms.CharField(label="Komentariu", required=True, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
    class Meta:
        model = EvalLetCNABack
        fields = ['number','subject','date','file','comment']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('number', css_class='form-group col-md-2 mb-0'),
                Column('subject', css_class='form-group col-md-4 mb-0'),
                Column('date', css_class='form-group col-md-3 mb-0'),
                Column('file', css_class='form-group col-md-3 mb-0'),
                
                css_class='form-row'
            ),
            Row(
                Column('comment', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
           
            HTML(""" <button class="btn btn-secondary" type="submit" title="Rai & Manda Fila"><i class="fa fa-reply"></i> Rai & Manda Fila</button> """)
        )