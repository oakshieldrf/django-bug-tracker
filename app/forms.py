from django import forms 


class IncidenciaForm(forms.Form): 
    nombre = forms.CharField(max_length=100)
    grado = forms.CharField(widget=forms.Select)
    descripcion = forms.CharField(widget=forms.Textarea)
    equipo = forms.CharField(widget=forms.Select)
    tipo = forms.CharField(widget=forms.Select)
    responsables = forms.CharField(widget=forms.Select)
    horas = forms.TimeField()


