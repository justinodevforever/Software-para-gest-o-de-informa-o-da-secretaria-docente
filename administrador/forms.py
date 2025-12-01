
from django import forms
from .models import *
from django.db.models import Q
import string, secrets

from django.shortcuts import get_list_or_404

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

    STATUS = [
        ('ativa', 'Ativa'),
        ('finalizada', 'Finalizada'),
    ]

    
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
        choices= STATUS,
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

    nome_mae = forms.CharField(
        required=True,
        widget= forms.TextInput()
    )
    nome_pai = forms.CharField(
        required=True,
        widget= forms.TextInput()
    )

    provincia = forms.CharField(
        required=True,
        widget= forms.TextInput()
    )
    municipio = forms.CharField(
        required=True,
        widget= forms.TextInput()
    )
    natural = forms.CharField(
        required=True,
        widget= forms.TextInput()
    )

    emitido_em = forms.CharField(
        required=True,
        widget= forms.TextInput()
    )
    endereco = forms.CharField(
        required=False,
        widget= forms.TextInput()
    )

    data_emissao = forms.DateField(
        required=True,
        widget= forms.DateInput()
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

    def save(self):

        

        estudante = Estudante(
            nome_completo = self.cleaned_data['nome_completo'],
            nome_mae = self.cleaned_data['nome_mae'],
            nome_pai = self.cleaned_data['nome_pai'],
            endereco = self.cleaned_data['endereco'],
            emitido_em = self.cleaned_data['emitido_em'],
            data_emissao = self.cleaned_data['data_emissao'],
            bi = self.cleaned_data['bi'],
            telefone = self.cleaned_data['telefone'],
            genero = self.cleaned_data['genero'],
            data_nascimento = self.cleaned_data['data_nascimento'],
            provincia = self.cleaned_data['provincia'],
            municipio = self.cleaned_data['municipio'],
            natural = self.cleaned_data['natural'],
        )

        matricula = Matricula(
            turma = self.cleaned_data['turma'],
            ano_letivo = self.cleaned_data['ano_letivo'],
            status_matricula = self.cleaned_data['status_matricula'],
        )

        return matricula, estudante
    
class MatriculaEditForm(forms.Form):

    
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
        widget= forms.Select(attrs={'id': 'status_matricula'})
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

    nome_mae = forms.CharField(
        required=True,
        widget= forms.TextInput()
    )
    nome_pai = forms.CharField(
        required=True,
        widget= forms.TextInput()
    )
    emitido_em = forms.CharField(
        required=False,
        widget= forms.TextInput()
    )
    provincia = forms.CharField(
        required=True,
        widget= forms.TextInput()
    )
    municipio = forms.CharField(
        required=True,
        widget= forms.TextInput()
    )
    natural = forms.CharField(
        required=True,
        widget= forms.TextInput()
    )
    endereco = forms.CharField(
        required=False,
        widget= forms.TextInput()
    )

    data_emissao = forms.DateField(
        required=False,
        widget= forms.DateInput()
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

        ano = AnoLetivo.objects.get(id=self.instance.ano_letivo.id)
        turma = Turma.objects.get(id=self.instance.turma.id)

    
        if self.instance:
            self.fields['ano_letivo'].initial = ano

        if self.instance:
            self.fields['turma'].initial = turma

        if self.instance:
            self.fields['status_matricula'].initial = self.instance.status_matricula

        if self.instance.data_cancelamento:
            self.fields['data_cancelamento'].initial = self.instance.data_cancelamento

        if self.instance.motivo_cancelamento:
            self.fields['motivo_cancelamento'].initial = self.instance.motivo_cancelamento

    def clean(self):
        status_matricula = self.cleaned_data['status_matricula']
        data_cancelamento = self.cleaned_data['data_cancelamento']
        motivo_cancelamento = self.cleaned_data['motivo_cancelamento']

        if status_matricula == 'cancelada' and not data_cancelamento:
            self.add_error('data_cancelamento', 'Opção cancelada foi selecionada, e este campo é Obrigatório!')

        if status_matricula == 'cancelada' and not motivo_cancelamento:
            self.add_error('motivo_cancelamento', 'Opção cancelada, é Obrigatório!')

    def save(self):

        self.instance.estudante.nome_completo = self.cleaned_data['nome_completo']
        self.instance.estudante.bi = self.cleaned_data['bi']
        self.instance.estudante.telefone = self.cleaned_data['telefone']
        self.instance.estudante.genero = self.cleaned_data['genero']
        self.instance.estudante.data_nascimento = self.cleaned_data['data_nascimento']
        self.instance.estudante.nome_mae = self.cleaned_data['nome_mae']
        self.instance.estudante.provincia = self.cleaned_data['provincia']
        self.instance.estudante.municipio = self.cleaned_data['municipio']
        self.instance.estudante.natural = self.cleaned_data['natural']
        self.instance.estudante.nome_pai = self.cleaned_data['nome_pai']
        self.instance.estudante.endereco = self.cleaned_data['endereco']
        self.instance.estudante.emitido_em = self.cleaned_data['emitido_em']
        self.instance.estudante.data_emissao = self.cleaned_data['data_emissao']

        self.instance.estudante.save()

        self.instance.turma = self.cleaned_data['turma']
        self.instance.ano_letivo = self.cleaned_data['ano_letivo']
        self.instance.status_matricula = self.cleaned_data['status_matricula']
        self.instance.data_cancelamento = self.cleaned_data['data_cancelamento']
        self.instance.motivo_cancelamento = self.cleaned_data['motivo_cancelamento']

        self.instance.save()


        return self.instance
    
class DisciplinaForm(forms.Form):

    
    professor = forms.ModelChoiceField(
        queryset=Professor.objects.all(),
        required=True, 
        widget= forms.Select()
    )

    classe = forms.ModelChoiceField(
        queryset=Classe.objects.all(),
        required=True, 
        widget= forms.Select()
    )

    nome = forms.CharField(
        required=True,
        widget= forms.TextInput(attrs={'id': 'nome'})
    )

    abreviatura = forms.CharField(
        required=False,
        widget= forms.TextInput(attrs={'id': 'abreviatura'})
    )


    def save(self):

        disciplina = Disciplina(
            nome = self.cleaned_data['nome'],
            professor = self.cleaned_data['professor'],
            classe = self.cleaned_data['classe'],
            abreviatura = self.cleaned_data['abreviatura'],
        )

        disciplina.save()

        return disciplina
    
class DisciplinaEditForm(forms.Form):

    
    professor = forms.ModelChoiceField(
        queryset=Professor.objects.all(),
        required=True, 
        widget= forms.Select()
    )

    classe = forms.ModelChoiceField(
        queryset=Classe.objects.all(),
        required=True, 
        widget= forms.Select()
    )

    nome = forms.CharField(
        required=True,
        widget= forms.TextInput(attrs={'id': 'nome'})
    )

    abreviatura = forms.CharField(
        required=False,
        widget= forms.TextInput(attrs={'id': 'abreviatura'})
    )

    def __init__(self, *args, **kwargs):
        self.disciplina = kwargs.pop('instance', None)

        super().__init__(*args, **kwargs)
     
        self.fields['professor'].initial = self.disciplina.professor
        self.fields['classe'].initial = self.disciplina.classe


    def save(self):

        self.disciplina.nome = self.cleaned_data['nome']
        self.disciplina.professor = self.cleaned_data['professor']
        self.disciplina.classe = self.cleaned_data['classe']
        self.disciplina.abreviatura = self.cleaned_data['abreviatura']

        self.disciplina.save()

        return self.disciplina
    
class TurmaForm(forms.Form):
    
    ano_letivo = forms.ModelChoiceField(
        queryset=AnoLetivo.objects.all(),
        required=True, 
        widget= forms.Select()
    )

    periodo = forms.ModelChoiceField(
        queryset=Periodo.objects.all(),
        required=True, 
        widget= forms.Select()
    )

    classe = forms.ModelChoiceField(
        queryset=Classe.objects.all(),
        required=True, 
        widget= forms.Select()
    )

    turma = forms.CharField(
        required=True,
        widget= forms.TextInput(attrs={
            'oninput': 'this.value=this.value.toUpperCase()',
            'placeholder': 'Nome da turma'
        })
    )


    def __init__(self, *args, **kwargs):
        self.turma = kwargs.pop('instance', None)

        super().__init__(*args, **kwargs)

        if self.turma is not None:

            self.fields['turma'].initial = self.turma.turma
            self.fields['ano_letivo'].initial = self.turma.ano_letivo
            self.fields['classe'].initial = self.turma.classe
            self.fields['periodo'].initial = self.turma.periodo
     
        
    def clean(self):
        turma=self.cleaned_data['turma']
        ano_letivo=self.cleaned_data['ano_letivo']
        classe=self.cleaned_data['classe']
        periodo=self.cleaned_data['periodo']

        if self.turma is None:
            try:

                if Turma.objects.filter( Q(turma=turma) & Q(ano_letivo=ano_letivo) & Q(classe=classe) & Q(periodo=periodo) ).exists():

                    self.add_error('turma', 'Está turma com essas informações já existe!')

            except Turma.DoesNotExist:
                pass

    def save(self):

        if self.turma is None:

            turma = Turma(
                turma=self.cleaned_data['turma'],
                ano_letivo=self.cleaned_data['ano_letivo'],
                classe=self.cleaned_data['classe'],
                periodo=self.cleaned_data['periodo'],
            )

            turma.save()

            return turma
       
        else:
           
            self.turma.turma=self.cleaned_data['turma']
            self.turma.ano_letivo=self.cleaned_data['ano_letivo']
            self.turma.classe=self.cleaned_data['classe']
            self.turma.periodo=self.cleaned_data['periodo']

            return self.turma
        
class ResultadoForm(forms.Form):
   
    estudante_id = forms.IntegerField(widget=forms.HiddenInput())

    not_Ev_Sist1 = forms.DecimalField(max_digits=5, decimal_places=2, required=True)
    not_Ev_Sist2 = forms.DecimalField(max_digits=5, decimal_places=2, required=True)
    not_Ev_Sist3 = forms.DecimalField(max_digits=5, decimal_places=2, required=True)
    not_Prov1 = forms.DecimalField(max_digits=5, decimal_places=2, required=True)
    not_Prov2 = forms.DecimalField(max_digits=5, decimal_places=2, required=True)
    not_Prov3 = forms.DecimalField(max_digits=5, decimal_places=2, required=True)
    not_examen = forms.DecimalField(max_digits=5, decimal_places=2, required=True)

def gerar_senha():

    caracter = string.ascii_letters + string.digits + '@#$%!&%'


    return ''.join(secrets.choice(caracter) for _ in range(9))

class UsuarioForm(forms.Form):
    
    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        required=True, 
        widget= forms.Select(attrs={'id': 'role'})
    )

    nome_completo = forms.CharField(
        required=True, 
        widget= forms.TextInput(attrs={'id': 'nome_completo', 'placeholder': 'Nome completo'})
    )

    email = forms.CharField(
        required=True,
        widget= forms.TextInput(attrs={'id': 'email', 'placeholder': 'E-mail'})
    )

    username = forms.CharField(
        required=True,
        widget= forms.TextInput(attrs={'id': 'username', 'placeholder': 'Nome do usuário'})
    )

    password = forms.CharField(
        required=True,
        widget= forms.PasswordInput(attrs={'id': 'password', 'placeholder': 'Senha'})
    )

    is_active = forms.BooleanField(
        required=False,
        widget= forms.CheckboxInput()
    )

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('instance', None)

        super().__init__(*args, **kwargs)

        if self.usuario:

            self.fields['username'].initial = self.usuario.username
            self.fields['nome_completo'].initial = self.usuario.nome_completo
            self.fields['email'].initial = self.usuario.email
            self.fields['role'].initial = self.usuario.role


    def save(self):

        if self.usuario is None:

            usuario = Usuario(
                username = self.cleaned_data['username'],
                nome_completo = self.cleaned_data['nome_completo'],
                role = self.cleaned_data['role'],
                email = self.cleaned_data['email'],
                is_active = True,
            )

            if self.cleaned_data['role'].nome == 1:
                usuario.is_staff = True
                usuario.is_superuser = True
            
            usuario.set_password(self.cleaned_data['password'])

            usuario.save()

            return usuario
        
        else:

            self.usuario.username = self.cleaned_data['username']
            self.usuario.nome_completo = self.cleaned_data['nome_completo']
            self.usuario.role = self.cleaned_data['role']
            self.usuario.email = self.cleaned_data['email']
            self.usuario.is_active = self.cleaned_data['is_active']

            if self.cleaned_data['role'].nome == 1:

                self.usuario.is_staff = True
                self.usuario.is_superuser = True

            else:
                self.usuario.is_staff = False
                self.usuario.is_superuser = False

            
            self.usuario.save()


            return self.usuario
        
class ClasseForm(forms.Form):
    
    denominacao = forms.CharField(
        required=False,
        widget= forms.TextInput(attrs={'id': 'denominacao', 'placeholder': 'Nome da classe'})
    )


    def __init__(self, *args, **kwargs):
        self.classe = kwargs.pop('instance', None)

        super().__init__(*args, **kwargs)

        if self.classe:

            self.fields['denominacao'].initial = self.classe.denominacao


    def save(self):

        if self.classe is None:
            

            classe = Classe(
                denominacao = self.cleaned_data['denominacao'],
            )



            classe.save()

            return classe
        
        else:

            self.classe.denominacao = self.cleaned_data['denominacao']

            return self.classe

class AnoLetivoForm(forms.Form):

    ano = forms.CharField(
        required=True, 
        widget= forms.TextInput(attrs={'id': 'ano'})
    )
    dataFim = forms.DateField(
        required=True, 
        widget= forms.DateInput(attrs={'id': 'dataFim'})
    )
    dataInicio = forms.DateField(
        required=True, 
        widget= forms.DateInput()
    )
    e_atual = forms.BooleanField(
        required=False, 
        widget= forms.CheckboxInput(attrs={'id': 'e_atual'})
    )

    def __init__(self, *args, **kwargs):
        self.ano_letivo = kwargs.pop('instance', None)

        super().__init__(*args, **kwargs)

        if self.ano_letivo:

            self.fields['ano'].initial = self.ano_letivo.ano
            self.fields['e_atual'].initial = self.ano_letivo.e_atual
            self.fields['dataInicio'].initial = self.ano_letivo.dataInicio
            self.fields['dataFim'].initial = self.ano_letivo.dataFim


    def save(self):

        if self.ano_letivo is None:

            ano_letivo = AnoLetivo(
                ano = self.cleaned_data['ano'],
                dataFim = self.cleaned_data['dataFim'],
                dataInicio = self.cleaned_data['dataInicio'],
                e_atual = self.cleaned_data['e_atual'],
            )

            ano_letivo.save()

            return ano_letivo
        
        else:

            self.ano_letivo.ano = self.cleaned_data['ano']
            self.ano_letivo.dataFim = self.cleaned_data['dataFim']
            self.ano_letivo.dataInicio = self.cleaned_data['dataInicio']
            self.ano_letivo.e_atual = self.cleaned_data['e_atual']

            self.ano_letivo.save()


            return self.ano_letivo


class HorarioAulaForm(forms.Form):

    turma = forms.ModelChoiceField(queryset=Turma.objects.all(), label="Turma")
    disciplina = forms.ModelChoiceField(queryset=Disciplina.objects.all(), label="Disciplina")
    professor = forms.ModelChoiceField(queryset=Professor.objects.all(), label="Professor")
    ano_letivo = forms.ModelChoiceField(queryset=AnoLetivo.objects.all(), label="Ano lectivo")
    dia_semana = forms.ChoiceField(
        choices=HorarioAula.DiaSemana.choices,
        label="Dia da Semana"
    )
    hora_inicio = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label="Hora Início")
    hora_fim = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label="Hora Fim")
    tipo = forms.ChoiceField(
        choices=[('prova', 'Prova'), ('aula', 'Aula')],
        label="Tipo",
    )
    data_prova = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label="Data da Prova"
    )
    sala = forms.CharField(max_length=50, label="Sala")

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        data_prova = cleaned_data.get('data_prova')

        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fim = cleaned_data.get('hora_fim')

        if hora_inicio > hora_fim:

            self.add_error('hora_inicio', 'Hora início não pode ser maior que hora final')

        if tipo == 'prova' and not data_prova:
            self.add_error('data_prova', 'A data da prova é obrigatória quando o tipo é Prova.')
            
        return cleaned_data
    

class ReconfirmacaoForm(forms.Form):

    
    turma = forms.ModelChoiceField(
        queryset=Turma.objects.all(),
        required=True, 
        widget= forms.Select()
    )
    bi = forms.CharField(
        required=True,
        widget= forms.TextInput(attrs={'placeholder': 'Digite B.I do estudante'})
    )

    def clean(self):
        clean_data =  super().clean()

        try:

            estudante = Estudante.objects.get(bi = self.cleaned_data['bi'])
        
        except Estudante.DoesNotExist:
            self.add_error('bi', 'Nenhum usuário encontrado com esse B.I')

        return clean_data
    
    def save(self):


        ano_letivo = AnoLetivo.objects.get(e_atual=True)

        try:

            estudante = Estudante.objects.get(bi = self.cleaned_data['bi'])

            matricula = Matricula(
                turma = self.cleaned_data['turma'],
                ano_letivo = ano_letivo,
                status_matricula = 'ativa',
                estudante=estudante
            )

            return matricula, estudante
        
        except Estudante.DoesNotExist:
            return self.add_error('bi', 'Nenhum usuário encontrado com esse B.I')
