
from django import forms
from .models import *

class ProfessorForm(forms.Form):

    nome_completo = forms.CharField(
        required=True,
        widget= forms.TextInput()
    )
    data_nascimento = forms.DateField(
        required=True,
        widget= forms.DateInput()
    )
    genero = forms.ChoiceField(
        choices= Professor.GENERO,
        required=True,
        widget= forms.Select()
    )
    telefone = forms.CharField(
        required=True,
        widget= forms.TextInput()
    )
    categoria = forms.ModelChoiceField(
        queryset= Categoria.objects.all(),
        required=True,
        widget= forms.Select()
    )

    def save(self, professor=None):

        if professor is None: 

            professor = Professor(
                nome_completo = self.cleaned_data['nome_completo'],
                categoria = self.cleaned_data['categoria'],
                telefone = self.cleaned_data['telefone'],
                genero = self.cleaned_data['genero'],
                data_nascimento = self.cleaned_data['data_nascimento'],
            )

            return professor
        
        else:
            professor.nome_completo = self.cleaned_data['nome_completo']
            professor.categoria = self.cleaned_data['categoria']
            professor.telefone = self.cleaned_data['telefone']
            professor.genero = self.cleaned_data['genero']
            professor.data_nascimento = self.cleaned_data['data_nascimento']

            return professor

class EstudanteForm(forms.Form):

    nome_completo = forms.CharField(
        required=True,
        widget= forms.TextInput()
    )
    data_nascimento = forms.DateField(
        required=True,
        widget= forms.DateInput()
    )
    genero = forms.ChoiceField(
        choices= Estudante.GENERO,
        required=True,
        widget= forms.Select()
    )
    telefone = forms.CharField(
        required=False,
        widget= forms.TextInput()
    )
    bi = forms.CharField(
        required=False,
        widget= forms.TextInput()
    )

    def save(self, estudante=None):

        if estudante is None: 

            estudante = Estudante(
                nome_completo = self.cleaned_data['nome_completo'],
                bi = self.cleaned_data['bi'],
                telefone = self.cleaned_data['telefone'],
                genero = self.cleaned_data['genero'],
                data_nascimento = self.cleaned_data['data_nascimento'],
            )

            return estudante
        
        else:
            estudante.nome_completo = self.cleaned_data['nome_completo']
            estudante.bi = self.cleaned_data['bi']
            estudante.telefone = self.cleaned_data['telefone']
            estudante.genero = self.cleaned_data['genero']
            estudante.data_nascimento = self.cleaned_data['data_nascimento']

            return estudante


class MatriculaForm(forms.Form):

    
    turma = forms.ModelChoiceField(
        queryset=Turma.objects.all(),
        required=True, 
        widget= forms.Select()
    )

    ano_letivo = forms.ModelChoiceField(
        queryset=AnoLetivo.objects.all(),
        required=True, 
        widget= forms.Select()
    )

    data_cancelamento = forms.DateField(
        required=False,
        widget= forms.DateInput()
    )

    status_matricula = forms.ChoiceField(
        choices= Matricula.STATUS,
        required=False,
        widget= forms.Select()
    )

    motivo_cancelamento = forms.CharField(
        required=False,
        widget= forms.Textarea()
    )


    nome_completo = forms.CharField(
        required=True,
        widget= forms.TextInput()
    )
    data_nascimento = forms.DateField(
        required=True,
        widget= forms.DateInput()
    )
    genero = forms.ChoiceField(
        choices= Estudante.GENERO,
        required=True,
        widget= forms.Select()
    )
    telefone = forms.CharField(
        required=False,
        widget= forms.TextInput()
    )
    bi = forms.CharField(
        required=False,
        widget= forms.TextInput()
    )

    def save(self, matricula=None):

        if matricula is None: 

            estudante = Estudante(
                nome_completo = self.cleaned_data['nome_completo'],
                bi = self.cleaned_data['bi'],
                telefone = self.cleaned_data['telefone'],
                genero = self.cleaned_data['genero'],
                data_nascimento = self.cleaned_data['data_nascimento'],
            )

            matricula = Matricula(
                turma = self.cleaned_data['turma'],
                ano_letivo = self.cleaned_data['ano_letivo'],
            )

            return matricula, estudante
        
        else:
            matricula.turma = self.cleaned_data['turma']
            matricula.data_cancelamento = self.cleaned_data['data_cancelamento']
            matricula.status_matricula = self.cleaned_data['status_matricula']
            matricula.motivo_cancelamento = self.cleaned_data['motivo_cancelamento']

            return matricula

