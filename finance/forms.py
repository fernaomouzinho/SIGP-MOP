from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML
from django.db.models import Q
from django_summernote.widgets import SummernoteWidget
from project.models import Project
from finance.models import CPV, CPVReq, CPVLetter, PO, POLetter, PRT, EV, TPO, FinFiles
from invoice.models import Invoice

class DateInput(forms.DateInput):
    input_type = 'date'

class CPVReqForm(forms.ModelForm):
    date = forms.DateField(label="Data", widget=DateInput(), required=False)
    class Meta:
        model = CPVReq
        fields = ['proj','subject','number','date','file']
        widgets = {
            'number': forms.TextInput(attrs={'placeholder': '0000'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proj'].queryset = Project.objects.filter(is_end=False).all().order_by('code')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('proj', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('number', css_class='form-group col-md-3 mb-0'),
                Column('subject', css_class='form-group col-md-9 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('date', css_class='form-group col-md-3 mb-0'),
                Column('file', css_class='form-group col-md-9 mb-0'),
                css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )

class CPVReqForm2(forms.ModelForm):
    comment = forms.CharField(label="Komentariu", required=True, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '250px'}}))
    class Meta:
        model = CPVReq
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

class CPVForm(forms.ModelForm):
    date = forms.DateField(label="Data", widget=DateInput(), required=False)
    class Meta:
        model = CPV
        fields = ['number','amount','date','file']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('number', css_class='form-group col-md-4 mb-0'),
                Column('date', css_class='form-group col-md-4 mb-0'),
                Column('amount', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('file', css_class='form-group col-md-12 mb-0'), css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )

class CPVForm2(forms.ModelForm):
    comment = forms.CharField(label="Komentariu", required=True, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '250px'}}))
    class Meta:
        model = CPV
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

class CPVLetterForm(forms.ModelForm):
    date = forms.DateField(label="Data", widget=DateInput(), required=False)
    class Meta:
        model = CPVLetter
        fields = ['number','subject','date','file']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('number', css_class='form-group col-md-3 mb-0'),
                Column('subject', css_class='form-group col-md-6 mb-0'),
                Column('date', css_class='form-group col-md-3 mb-0'), css_class='form-row'
            ),
            Row(
                Column('file', css_class='form-group col-md-12 mb-0'), css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )
###
class POForm(forms.ModelForm):
    date = forms.DateField(label="Data", widget=DateInput(), required=False)
    class Meta:
        model = PO
        fields = ['cpv','number','amount','desc','date','file']
    def __init__(self, proj, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cpv'].queryset = CPV.objects.filter(proj=proj).all()
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('cpv', css_class='form-group col-md-3 mb-0'),
                Column('number', css_class='form-group col-md-3 mb-0'),
                Column('amount', css_class='form-group col-md-3 mb-0'),
                Column('date', css_class='form-group col-md-3 mb-0'), 
                css_class='form-row'
            ),
            Row(
                Column('file', css_class='form-group col-md-12 mb-0'), css_class='form-row'
            ),
            Row(
                Column('desc', css_class='form-group col-md-12 mb-0'), css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )

class POForm2(forms.ModelForm):
    class Meta:
        model = PO
        fields = ['inv']
    def __init__(self, cont, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['inv'].queryset = Invoice.objects.filter(cont=cont, is_end=False).all()
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('inv', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )

class POForm3(forms.ModelForm):
    comment = forms.CharField(label="Komentariu", required=True, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '250px'}}))
    class Meta:
        model = PO
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

class POLetterForm(forms.ModelForm):
    date = forms.DateField(label="Data", widget=DateInput(), required=False)
    class Meta:
        model = POLetter
        fields = ['number','subject','date','file']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('number', css_class='form-group col-md-3 mb-0'),
                Column('subject', css_class='form-group col-md-6 mb-0'),
                Column('date', css_class='form-group col-md-3 mb-0'), css_class='form-row'
            ),
            Row(
                Column('file', css_class='form-group col-md-12 mb-0'), css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )

class opPOForm(forms.ModelForm):
    date = forms.DateField(label="Data", widget=DateInput(), required=False)
    class Meta:
        model = PO
        fields = ['cpv','inv','number','amount','desc','date','file']
    def __init__(self, proj, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cpv'].queryset = CPV.objects.filter(proj=proj).all()
        self.fields['inv'].queryset = Invoice.objects.filter(cont__project=proj).all()
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('cpv', css_class='form-group col-md-3 mb-0'),
                Column('inv', css_class='form-group col-md-3 mb-0'),
                Column('number', css_class='form-group col-md-3 mb-0'),
                Column('amount', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('date', css_class='form-group col-md-3 mb-0'), 
                Column('file', css_class='form-group col-md-9 mb-0'), css_class='form-row'
            ),
            Row(
                Column('desc', css_class='form-group col-md-12 mb-0'), css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )
###
class PRTForm(forms.ModelForm):
    date = forms.DateField(label="Data", widget=DateInput(), required=False)
    class Meta:
        model = PRT
        fields = ['number','date','total','percent','file']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('number', css_class='form-group col-md-3 mb-0'),
                Column('date', css_class='form-group col-md-3 mb-0'),
                Column('total', css_class='form-group col-md-3 mb-0'),
                Column('percent', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('file', css_class='form-group col-md-12 mb-0'), css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )

class PRTForm2(forms.ModelForm):
    date = forms.DateField(label="Data", widget=DateInput(), required=False)
    class Meta:
        model = PRT
        fields = ['inv','number','date','total','percent','file']
    def __init__(self, proj, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['inv'].queryset = Invoice.objects.filter(project=proj, is_end=False).all()
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('number', css_class='form-group col-md-3 mb-0'),
                Column('date', css_class='form-group col-md-3 mb-0'),
                Column('total', css_class='form-group col-md-3 mb-0'),
                Column('percent', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('file', css_class='form-group col-md-12 mb-0'), css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )
###
class EVForm(forms.ModelForm):
    date = forms.DateField(label="Data", widget=DateInput(), required=True)
    class Meta:
        model = EV
        fields = ['number','date','file']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('number', css_class='form-group col-md-3 mb-0'),
                Column('date', css_class='form-group col-md-3 mb-0'),
                Column('file', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )
###
class TPOForm(forms.ModelForm):
    date = forms.DateField(label="Data", widget=DateInput(), required=False)
    class Meta:
        model = TPO
        fields = ['number','amount','date']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('number', css_class='form-group col-md-4 mb-0'),
                Column('amount', css_class='form-group col-md-4 mb-0'),
                Column('date', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
        )
###
class FinFilesForm(forms.ModelForm):
    class Meta:
        model = FinFiles
        fields = ['desc','file']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
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
