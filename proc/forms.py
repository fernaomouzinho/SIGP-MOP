from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.db.models import Q
from project.models import Project
from proc.models import Proc, ProcComp, ProcLet, ProcTrack, ProcFiles, ProcReqTrack, ProcResTrack
from django_summernote.widgets import SummernoteWidget

class DateInput(forms.DateInput):
    input_type = 'date'

class ProcForm(forms.ModelForm):
    date = forms.DateField(label="Data", widget=DateInput(), required=True)
    desc = forms.CharField(label="Deskrisaun", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
    class Meta:
        model = Proc
        fields = ['proj','number','date','desc']
        widgets = {
            'number': forms.TextInput(attrs={'placeholder': '0000'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proj'].queryset = Project.objects.filter(is_eval=True, is_cont=False).all().order_by('-year','-id')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('proj', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
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

class ProcCompForm(forms.ModelForm):
    submit_date = forms.DateField(widget=DateInput(), required=False)
    class Meta:
        model = ProcComp
        fields = ['company','submit_date','best']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('company', css_class='form-group col-md-7 mb-0'),
                Column('submit_date', css_class='form-group col-md-3 mb-0'),
                Column('best', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )

class ProcTrackForm(forms.ModelForm):
    date_announce = forms.DateField(label="Data Anuncia", widget=DateInput(), required=False)
    date_open = forms.DateField(label="Data Open Bid", widget=DateInput(), required=False)
    date_eval = forms.DateField(label="Data Avalia", widget=DateInput(), required=False)
    date_result = forms.DateField(label="Data Resultadu", widget=DateInput(), required=False)
    date_end = forms.DateField(label="Data Anuncia", widget=DateInput(), required=False)
    class Meta:
        model = ProcTrack
        fields = ['is_announce','date_announce','is_open','date_open',\
            'is_eval','date_eval','is_result','date_result']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('is_announce', css_class='form-group col-md-3 mb-0'),
                Column('date_announce', css_class='form-group col-md-3 mb-0'),
                Column('is_open', css_class='form-group col-md-3 mb-0'),
                Column('date_open', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('is_eval', css_class='form-group col-md-3 mb-0'),
                Column('date_eval', css_class='form-group col-md-3 mb-0'),
                Column('is_result', css_class='form-group col-md-3 mb-0'),
                Column('date_result', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )

class ProcLetForm(forms.ModelForm):
    date = forms.DateField(label="Data", widget=DateInput(), required=True)
    desc = forms.CharField(label="Deskrisaun", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
    class Meta:
        model = ProcLet
        fields = ['number','subject','date','to','desc','file']
        widgets = {
            'number': forms.TextInput(attrs={'placeholder': '0000'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('subject', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('number', css_class='form-group col-md-4 mb-0'),
                Column('date', css_class='form-group col-md-4 mb-0'),
                Column('to', css_class='form-group col-md-4 mb-0'),
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

class ProcLetForm2(forms.ModelForm):
    comment = forms.CharField(label="Komentariu", required=True, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
    class Meta:
        model = ProcLet
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
            HTML(""" <button class="btn btn-secondary" type="submit" title="Rai & Manda Fila"><i class="fa fa-reply"></i> Guarda & Manda Fila</button> """)
        )

class ProcFilesForm(forms.ModelForm):
    class Meta:
        model = ProcFiles
        fields = ['desc','file']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
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
