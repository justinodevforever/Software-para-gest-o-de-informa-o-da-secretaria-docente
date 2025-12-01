from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.dispatch import receiver
from datetime import date

class Role(models.Model):

    NAME_STATUS = [
        
        (1, 'Admin'),
        (2, 'Diretor'),
        (3, 'Secretário'),
        
    ]

    nome = models.IntegerField(max_length=90, choices=NAME_STATUS)

    def __str__(self):

        return f'{self.get_nome_display()}'

class Usuario(AbstractUser):

    nome_completo = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nome Completo')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)

    REQUIRED_FIELDS = ['nome_completo']
    
    def __str__(self):
        return f'{self.nome_completo}'


class Classe(models.Model):

    denominacao = models.CharField(max_length=15)

    def __str__(self):
        return self.denominacao

class Periodo(models.Model):

    periodo = models.CharField(max_length=60)

    def __str__(self):
        return self.periodo

class AnoLetivo(models.Model):

    ano = models.CharField(max_length=10)

    dataInicio = models.DateField(blank=True, null=True)
    dataFim = models.DateField(blank=True, null=True)
    e_atual = models.BooleanField(default=False)

    def __str__(self):
        return self.ano


class Turma(models.Model):

    turma = models.CharField(max_length=4)
    ano_letivo = models.ForeignKey(AnoLetivo, on_delete=models.SET_NULL, null=True, blank=True)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.turma}-{self.classe.denominacao}-{self.periodo}-{self.ano_letivo}'

class Categoria(models.Model):

    categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.categoria

class Professor(models.Model):

    GENERO = [

        ('F', 'Feminino'),
        ('M', 'Masculino'),
        ('outro', 'Outro'),
        
    ]

    nome_completo = models.CharField(max_length=90)
    data_nascimento = models.DateField()
    genero = models.CharField(max_length=10, choices=GENERO)
    telefone = models.CharField(max_length=20)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    @property
    def idade(self):
        hoje = date.today()

        return hoje.year - self.data_nascimento.year -(
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )
    

    def __str__(self):
        return self.nome_completo

class Disciplina(models.Model):

    nome = models.CharField(max_length=90)
    abreviatura = models.CharField(max_length=10, blank=True, null=True)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nome}'

class Estudante(models.Model):
    GENERO = [
    
        ('F', 'Feminino'),
        ('M', 'Masculino'),
        ('outro', 'Outro'),
        
    ]

    nome_completo = models.CharField(max_length=100)
    nome_mae = models.CharField(max_length=100)
    nome_pai = models.CharField(max_length=100)
    
    natural = models.CharField(max_length=100, blank=True, null=True)
    provincia = models.CharField(max_length=100, blank=True, null=True)
    municipio = models.CharField(max_length=100, blank=True, null=True)

    data_nascimento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=8, choices=GENERO)
    bi = models.CharField(max_length=14, blank=True, null=True)
    data_emissao = models.DateField(null=True, blank=True)
    emitido_em = models.CharField(max_length=100,  blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)

    data_criacao = models.DateTimeField(auto_now_add=True)

    @property
    def idade(self):
        hoje = date.today()

        return hoje.year - self.data_nascimento.year -(
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )
    

    def __str__(self):
        return self.nome_completo

class Matricula(models.Model):

    STATUS = [
        ('ativa', 'Ativa'),
        ('desistente', 'Desistente'),
        ('cancelada', 'Cancelada'),
        ('finalizada', 'Finalizada'),
    ]

    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    ano_letivo = models.ForeignKey(AnoLetivo, on_delete=models.CASCADE)
    data_matricula = models.DateTimeField(auto_now_add=True)
    status_matricula  = models.CharField(max_length=60, choices=STATUS, default='ativa')
    data_cancelamento = models.DateField(blank=True, null=True)
    motivo_cancelamento = models.TextField(blank=True, null=True)

    criado_por = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.estudante.nome_completo
    
class Resultado(models.Model):

    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    not_Ev_Sist1 = models.DecimalField(max_digits=5, decimal_places=2)
    not_Ev_Sist2 = models.DecimalField(max_digits=5, decimal_places=2)
    not_Ev_Sist3 = models.DecimalField(max_digits=5, decimal_places=2)
    not_Prov1 = models.DecimalField(max_digits=5, decimal_places=2)
    not_Prov2= models.DecimalField(max_digits=5, decimal_places=2)
    not_Prov3 = models.DecimalField(max_digits=5, decimal_places=2)
    not_examen = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.estudante.nome_completo


class HorarioAula(models.Model):
    class DiaSemana(models.TextChoices):
        SEGUNDA = 'Segunda', 'Segunda-feira'
        TERCA = 'Terça', 'Terça-feira'
        QUARTA = 'Quarta', 'Quarta-feira'
        QUINTA = 'Quinta', 'Quinta-feira'
        SEXTA = 'Sexta', 'Sexta-feira'

    turma = models.ForeignKey('Turma', on_delete=models.CASCADE, related_name='horarios')
    disciplina = models.ForeignKey('Disciplina', on_delete=models.CASCADE, related_name='horarios')
    ano_letivo = models.ForeignKey('AnoLetivo', on_delete=models.CASCADE, related_name='horarios')
    professor = models.ForeignKey('Professor', on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.CharField(max_length=10, choices=DiaSemana.choices)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    tipo = models.CharField(max_length=20, choices=[
        ('prova', 'Prova'),
        ('aula', 'Aula')
    ])
    data_prova = models.DateField(blank=True, null=True)
    sala = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.turma} - {self.disciplina} ({self.dia_semana} {self.hora_inicio}-{self.hora_fim})"    