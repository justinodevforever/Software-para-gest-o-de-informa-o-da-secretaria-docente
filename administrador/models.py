from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

from datetime import date

class Role(models.Model):

    NAME_STATUS = [
        
        (1, 'Admin'),
        (3, 'Secretário'),
        (2, 'Diretor'),
        (4, 'Estudante'),
        
    ]

    nome = models.IntegerField(max_length=90, choices=NAME_STATUS)

    def __str__(self):

        return f'{self.get_nome_display()}'
    
class Usuario(AbstractUser):

    nome_completo = models.CharField(max_length=100, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome_completo

    
class Instituicao(models.Model):

    nome = models.CharField(max_length=90)

    def __str__(self):
        return self.nome

class Classe(models.Model):

    denominacao = models.CharField(max_length=15)
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE)

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

    def __str__(self):
        return self.ano

class AnoEscolar(models.Model):

    ano = models.CharField(max_length=10)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    ano_letivo = models.ForeignKey(AnoLetivo, on_delete=models.CASCADE)

    def __str__(self):
        return self.ano


class Turma(models.Model):

    turma = models.CharField(max_length=4)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.turma}-{self.classe.denominacao}'



class Disciplina(models.Model):

    nome = models.CharField(max_length=90)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Estudante(models.Model):
    GENERO = [
    
        ('F', 'Feminino'),
        ('M', 'Masculino'),
        ('outro', 'Outro'),
        
    ]

    nome_completo = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    genero = models.CharField(max_length=8, choices=GENERO)
    bi = models.CharField(max_length=14, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

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
    not_Ev_Sist2 = models.DecimalField(max_digits=5, decimal_places=2)
    not_Prov1 = models.DecimalField(max_digits=5, decimal_places=2)
    not_Prov2= models.DecimalField(max_digits=5, decimal_places=2)
    not_Prov3 = models.DecimalField(max_digits=5, decimal_places=2)
    not_examen = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.estudante.nome_completo


class Categoria(models.Model):

    categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.categoria

class Habilitacao(models.Model):

    habilitacao = models.CharField(max_length=100)

    def __str__(self):
        return self.habilitacao

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

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    @property
    def idade(self):
        hoje = date.today()

        return hoje.year - self.data_nascimento.year -(
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )
    

    def __str__(self):
        return self.nome_completo
    
class DisciplinaProfessor(models.Model):

    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    def __str__(self):
        return self.disciplina