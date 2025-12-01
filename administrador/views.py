from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Prefetch, ExpressionWrapper, F, CharField, FloatField, Case, When, Value, Avg
from django.views.decorators.http import require_http_methods

from .models import *
from .forms import *
import math, base64, os
from django.conf import settings
from decimal import Decimal
from datetime import datetime
from xhtml2pdf import pisa

from django.contrib import messages

@login_required
def index(request):

    total_matricula = Matricula.objects.all().count()
    total_professor = Professor.objects.all().count()
    total_turma = Turma.objects.all().count()
    total_matricula_finalizada = Matricula.objects.filter(status_matricula='finalizada').count()


    disciplinas = Disciplina.objects.all()
    disciplinas = Disciplina.objects.all()
    labels = [d.nome for d in disciplinas]
    data = []

    for d in disciplinas:
        media = Resultado.objects.filter(disciplina=d).annotate(
            media_aluno=ExpressionWrapper(
                (F('not_Ev_Sist1') + F('not_Ev_Sist2') + F('not_Ev_Sist3') +
                F('not_Prov1') + F('not_Prov2') + F('not_Prov3') + F('not_examen')) / 7.0,
                output_field=FloatField()
            )
        ).aggregate(media_disciplina=Avg('media_aluno'))['media_disciplina'] or 0
        data.append(media)

    context = {
        'total_matricula': total_matricula,
        'total_matricula_finalizada': total_matricula_finalizada,
        'total_professor': total_professor,
        'total_turma': total_turma,
        'labels_chart': labels,
        'data_chart': data,
    } 

    return render(request, 'index.html', context)

@login_required
def criar_professor(request):

    form = ProfessorForm()

    if request.method == 'POST':

        form = ProfessorForm(request.POST)

        if form.is_valid():

            professor = form.save()

            professor.usuario = request.user

            professor.save()

            context = {
                'sucesso': 'Professor Criado com sucesso!',
                'form': form
            }


            return render(request, 'professor/criar_professor.html', context)
        
        else:
            context = {
                'erro': 'Erro ao Criar o Professor, verifique as informações abaixo!',
                'form': form
            }
            return render(request, 'professor/criar_professor.html', context)
    else:

        form = ProfessorForm()
        return render(request, 'professor/criar_professor.html', {'form': form} )
    
@login_required
def editar_professor(request, id):

    professor = Professor.objects.get(id=id)
    categorias = Professor.objects.all()

    form = ProfessorForm()

    professor.data_nascimento = professor.data_nascimento.strftime('%Y-%m-%d')

    if request.method == 'POST':

        form = ProfessorForm(request.POST)

        if form.is_valid():

            professor = form.save(professor=professor)

            professor.save()

            professor.data_nascimento = professor.data_nascimento.strftime('%Y-%m-%d')

            context = {
                'sucesso': 'Atualização do Professor feita com sucesso!',
                'form': form,
                'categorias': categorias,
                'professor': professor
            }


            return render(request, 'professor/editar_professor.html', context)
        
        else:
            context = {
                'erro': 'Erro ao Atualizar dados do Professor, verifique as informações abaixo!',
                'form': form,
                'categorias': categorias,
                'professor': professor
            }
            return render(request, 'professor/editar_professor.html', context)
    else:

        form = ProfessorForm()

        context = {
            'form': form,
            'categorias': categorias,
            'professor': professor
        }

        return render(request, 'professor/editar_professor.html', context)

@login_required
def lista_professor(request):

    professores = Professor.objects.all()

    per_page = request.GET.get('per_page', 20)
    page = request.GET.get('page', 1)
    order_by = request.GET.get('order_by', 'nome_completo')
    nome_filter = request.GET.get('nome_filter')


    if nome_filter:

        nome_filter = nome_filter.strip()
        professores = professores.filter(nome_completo__icontains=nome_filter)

    professores = professores.order_by(order_by)

    paginator = Paginator(professores, per_page)

    obj = paginator.page(page)


    context = {
        'professores': obj,
        'order_by': order_by,
        'nome_filter': nome_filter,
        'per_page': per_page
    }
    return render(request, 'professor/lista_professor.html', context)

@login_required
def visualizar_professor(request, id):

    professor = Professor.objects.get(id=id)


    return render(request, 'professor/visualizar_professor.html', {'professor': professor})

@login_required
@require_http_methods('POST')
def delete_professor(request, id):

    professor = Professor.objects.get(id=id)

    dados = json.loads(request.body)
    password = dados.get('password')
    user = request.user

    if not user.check_password(password.strip()):

        return JsonResponse({'erro': 'Credinciais inválidas'}, status=403)
    
    professor.delete()

    return redirect('lista_professor')


@login_required
def lista_estudante(request):

    estudantes = Estudante.objects.all()

    per_page = request.GET.get('per_page', 20)
    page = request.GET.get('page', 1)
    order_by = request.GET.get('order_by', '-data_criacao')
    nome_filter = request.GET.get('nome_filter')


    if nome_filter:

        nome_filter = nome_filter.strip()
        estudantes = estudantes.filter(nome_completo__icontains=nome_filter)

    estudantes = estudantes.order_by(order_by)

    paginator = Paginator(estudantes, per_page)

    obj = paginator.page(page)


    context = {
        'estudantes': obj,
        'order_by': order_by,
        'nome_filter': nome_filter,
        'per_page': per_page
    }
    return render(request, 'estudante/lista_estudante.html', context)

@login_required
def editar_estudante(request, id):

    estudante = Estudante.objects.get(id=id)

    form = EstudanteForm()

    estudante.data_nascimento = estudante.data_nascimento.strftime('%Y-%m-%d')

    if request.method == 'POST':

        form = EstudanteForm(request.POST)

        if form.is_valid():

            estudante = form.save(estudante=estudante)

            estudante.save()

            estudante.data_nascimento = estudante.data_nascimento.strftime('%Y-%m-%d')

            context = {
                'sucesso': 'Atualização do estudante feita com sucesso!',
                'form': form,
                'estudante': estudante
            }


            return render(request, 'estudante/editar_estudante.html', context)
        
        else:
            context = {
                'erro': 'Erro ao Atualizar dados do estudante, verifique as informações abaixo!',
                'form': form,
                'estudante': estudante
            }
            return render(request, 'estudante/editar_estudante.html', context)
    else:

        form = EstudanteForm()

        context = {
            'form': form,
            'estudante': estudante
        }

        return render(request, 'estudante/editar_estudante.html', context)
    
@login_required
def visualizar_estudante(request, id):

    estudante = Estudante.objects.get(id=id)
    ano_letivo = AnoLetivo.objects.get(e_atual=True)

    matricula = ''

    try:
        matricula = Matricula.objects.get(
            estudante=estudante,
            status_matricula='ativa',
            ano_letivo=ano_letivo
        )
        
    except Matricula.DoesNotExist:
        pass


    return render(request, 'estudante/visualizar_estudante.html', {'estudante': estudante, 'matricula': matricula})

@login_required
def reconfirmacao(request):

    form = ReconfirmacaoForm()

    if request.method == 'POST':

        form = ReconfirmacaoForm(request.POST)

        if form.is_valid():

            matricula, estudante = form.save()

            user = request.user

            matricula.criado_por = user

            try:

                mat = Matricula.objects.filter(status_matricula='ativa')

                for m in mat:

                    m.status_matricula = 'finalizada'

                    m.save()

            except Matricula.DoesNotExist:
                pass

            matricula.save()

            context = {
                'sucesso': 'Reconfirmação realizada com sucesso!',
                'form': form
            }

            return render(request, 'reconfirmacao/criar_reconfirmacao.html', context)
        
        else:
            context = {
                'erro': 'Erro ao reconfirmar, corrija os erros abaixo',
                'form': form
            }

            return render(request, 'reconfirmacao/criar_reconfirmacao.html', context)
    else:

        context = {
            'form': form
        }

        return render(request, 'reconfirmacao/criar_reconfirmacao.html', context)
    
@login_required
def criar_matricula(request):

    form = MatriculaForm()

    if request.method == 'POST':

        form = MatriculaForm(request.POST)

        if form.is_valid():

            matricula, estudante = form.save()

            estudante.usuario = request.user
            estudante.save()

            matricula.criado_por = request.user
            matricula.estudante = estudante

            matricula.save()

            context = {
                'sucesso': 'Matrícula Criado com sucesso!',
                'form': form
            }


            return render(request, 'matricula/criar_matricula.html', context)
        
        else:
            context = {
                'erro': 'Erro ao Criar o Matrícula, verifique as informações abaixo!',
                'form': form
            }
            return render(request, 'matricula/criar_matricula.html', context)
    else:

        form = MatriculaForm()

        return render(request, 'matricula/criar_matricula.html', {'form': form} )
    

@login_required
def editar_matricula(request, id):

    matricula = Matricula.objects.get(id=id)

    if request.method == 'POST':

        form = MatriculaEditForm(request.POST, instance=matricula)

        if form.is_valid():

            form.save()

            matricula.save()

            if matricula.data_cancelamento:
                matricula.data_cancelamento = matricula.data_cancelamento.strftime('%Y-%m-%d')

            if matricula.estudante.data_emissao:
                matricula.estudante.data_emissao = matricula.estudante.data_emissao.strftime('%Y-%m-%d')

            matricula.estudante.data_nascimento = matricula.estudante.data_nascimento.strftime('%Y-%m-%d')

            context = {
                'sucesso': 'Matrícula atualizada com sucesso!',
                'form': form,
                'matricula': matricula
            }

            return render(request, 'matricula/editar_matricula.html', context)
        
        else:

            if matricula.data_cancelamento:
                matricula.data_cancelamento = matricula.data_cancelamento.strftime('%Y-%m-%d')

            if matricula.estudante.data_emissao:
                matricula.estudante.data_emissao = matricula.estudante.data_emissao.strftime('%Y-%m-%d')

            matricula.estudante.data_nascimento = matricula.estudante.data_nascimento.strftime('%Y-%m-%d')

            context = {
                'erro': 'Erro ao atualizar o matrícula, verifique as informações abaixo!',
                'form': form,
                'matricula': matricula
            }
            return render(request, 'matricula/editar_matricula.html', context)
    else:

        form = MatriculaEditForm(instance=matricula)

        if matricula.data_cancelamento:
            matricula.data_cancelamento = matricula.data_cancelamento.strftime('%Y-%m-%d')

        if matricula.estudante.data_emissao:
            matricula.estudante.data_emissao = matricula.estudante.data_emissao.strftime('%Y-%m-%d')

        matricula.estudante.data_nascimento = matricula.estudante.data_nascimento.strftime('%Y-%m-%d')

        return render(request, 'matricula/editar_matricula.html', {'form': form, 'matricula': matricula} )
    
@login_required
def lista_matricula(request):

    matriculas = Matricula.objects.all()

    per_page = request.GET.get('per_page', 20)
    page = request.GET.get('page', 1)
    order_by = request.GET.get('order_by', '-data_matricula')
    nome_filter = request.GET.get('nome_filter')


    if nome_filter:

        nome_filter = nome_filter.strip()
        matriculas = matriculas.filter(estudante__nome_completo__icontains=nome_filter)

    matriculas = matriculas.order_by(order_by)

    paginator = Paginator(matriculas, per_page)

    obj = paginator.page(page)


    context = {
        'matriculas': obj,
        'order_by': order_by,
        'nome_filter': nome_filter,
        'per_page': per_page
    }
    return render(request, 'matricula/lista_matricula.html', context)

def visualizar_matricula(request, id):

    matricula = Matricula.objects.get(id=id)

    return render(request, 'matricula/visualizar_matricula.html', {'matricula': matricula})


def listar_disciplina(request):

    disciplinas = Disciplina.objects.all()

    per_page = request.GET.get('per_page', 20)
    page = request.GET.get('page', 1)
    order_by = request.GET.get('order_by', 'nome')
    nome_filter = request.GET.get('nome_filter')


    if nome_filter:

        nome_filter = nome_filter.strip()
        disciplinas = disciplinas.filter(
            Q(nome__icontains=nome_filter) |
            Q(abreviatura=nome_filter)
        )

    disciplinas = disciplinas.order_by(order_by)

    paginator = Paginator(disciplinas, per_page)

    obj = paginator.page(page)


    context = {
        'disciplinas': obj,
        'order_by': order_by,
        'nome_filter': nome_filter,
        'per_page': per_page
    }
    return render(request, 'disciplina/listar_disciplina.html', context)


def criar_disciplina(request):

    form = DisciplinaForm()

    if request.method == 'POST':

        form = DisciplinaForm(request.POST)

        if form.is_valid():

            disciplina = form.save()

            context = {
                'sucesso': 'Disciplina Criada com sucesso!',
                'form': form
            }


            return render(request, 'disciplina/criar_disciplina.html', context)
        
        else:
            context = {
                'erro': 'Erro ao ariar a disciplina, verifique as informações abaixo!',
                'form': form
            }
            return render(request, 'disciplina/criar_disciplina.html', context)


    return render(request, 'disciplina/criar_disciplina.html', {'form': form})


def visualizar_disciplina(request, id):

    disciplina = Disciplina.objects.get(id=id)

    return render(request, 'disciplina/visualizar_disciplina.html', {'disciplina': disciplina})

def editar_disciplina(request, id):

    disciplina = Disciplina.objects.get(id=id)

    form = DisciplinaEditForm(instance=disciplina)

    if request.method == 'POST':

        form = DisciplinaEditForm(request.POST, instance=disciplina)

        if form.is_valid():

            disciplina = form.save()

            context = {
                'sucesso': 'Disciplina Criada com sucesso!',
                'form': form,
                'disciplina': disciplina
            }


            return render(request, 'disciplina/editar_disciplina.html', context)
        
        else:
            context = {
                'erro': 'Erro ao ariar a disciplina, verifique as informações abaixo!',
                'form': form,
                'disciplina': disciplina
            }
            return render(request, 'disciplina/editar_disciplina.html', context)

    context = {
                'form': form,
                'disciplina': disciplina
            }
    return render(request, 'disciplina/editar_disciplina.html', context)

@login_required
@require_http_methods('POST')
def delete_disciplina(request, id):

    disciplina = Disciplina.objects.get(id=id)

    dados = json.loads(request.body)
    password = dados.get('password')
    user = request.user

    if not user.check_password(password.strip()):

        return JsonResponse({'erro': 'Credinciais inválidas'}, status=403)
    
    disciplina.delete()

    return redirect('listar_disciplina')

@login_required
def listar_turma(request):

    turmas = Turma.objects.filter(ano_letivo__e_atual=True)
    ano_letivos = AnoLetivo.objects.all()

    per_page = request.GET.get('per_page', 20)
    page = request.GET.get('page', 1)
    order_by = request.GET.get('order_by', 'turma')
    nome_filter = request.GET.get('nome_filter')

    ano_letivo = AnoLetivo.objects.filter(e_atual=True).first()
    if nome_filter:
        ano_letivo = AnoLetivo.objects.get(id=nome_filter)

        nome_filter = nome_filter.strip()

        turmas = ''

        try:
            turmas = Turma.objects.filter(
                ano_letivo=nome_filter
            )

        except Turma.DoesNotExist:

           pass
        

    turmas = turmas.order_by(order_by)

    paginator = Paginator(turmas, per_page)

    obj = paginator.page(page)


    context = {
        'turmas': obj,
        'ano_letivos': ano_letivos,
        'ano_letivo': ano_letivo,
        'order_by': order_by,
        'nome_filter': nome_filter,
        'per_page': per_page
    }
    return render(request, 'turma/listar_turma.html', context)

@login_required
def listar_turma_estudantes(request, id_turma):

    ano_letivos = AnoLetivo.objects.all()

    try:

        turma = Turma.objects.get(
            Q(id=id_turma) &
            Q(ano_letivo__e_atual=True)
        )

    except Turma.DoesNotExist:
        turma = Turma.objects.get(
            Q(id=id_turma) &
            Q(ano_letivo__e_atual=False)
        )

    total_disciplina = Disciplina.objects.filter(classe=turma.classe).count()
    matriculas = Matricula.objects.filter(
        turma=turma
    )

    per_page = request.GET.get('per_page', 20)
    page = request.GET.get('page', 1)
    order_by = request.GET.get('order_by', '-data_matricula')
    nome_filter = request.GET.get('nome_filter')

    if nome_filter:

        try:
            turma = Turma.objects.get(
                Q(id=id_turma) &
                Q(ano_letivo=nome_filter)
            )

            total_disciplina = Disciplina.objects.filter(classe=turma.classe).count()
            matriculas = Matricula.objects.filter(
                turma=turma
            )

        except Turma.DoesNotExist:
            matriculas = Matricula.objects.filter(
                turma=turma
            )

    if order_by == 'nome_completo':
        matriculas = matriculas.order_by(estudante__nome_completo = order_by)

    else:
        matriculas = matriculas.order_by(order_by)

    paginator = Paginator(matriculas, per_page)

    obj = paginator.page(page)

    ano_letivo = ''
    if matriculas:
        ano_letivo = matriculas[0].ano_letivo

    else:
        if nome_filter:
            ano_letivo = AnoLetivo.objects.get(id=nome_filter)

    context = {
        'ano_letivos': ano_letivos,
        'matriculas': obj,
        'total_disciplina': total_disciplina,
        'turma': turma,
        'ano_letivo': ano_letivo,
        'id_turma': id_turma,
        'order_by': order_by,
        'nome_filter': nome_filter,
        'per_page': per_page
    }
    return render(request, 'lista_turma_estudante/listar_turma_estudantes.html', context)

@login_required
def detalhes_turma_estudantes(request, id_estudante, id_turma):

    estudante = Estudante.objects.get(id=id_estudante)
    turma = Turma.objects.get(id=id_turma)

    disciplinas = Disciplina.objects.filter(classe=turma.classe).prefetch_related(
        Prefetch(
            'resultado_set',
            queryset=Resultado.objects.filter(
                Q(estudante=estudante) &
                Q(turma=turma)
            ).select_related('turma','estudante').annotate(
                media_avaliacao=ExpressionWrapper(
                    (F('not_Ev_Sist1')+F('not_Ev_Sist2') + F('not_Ev_Sist3'))/3,
                    output_field=FloatField()
                ),
                media_prova=ExpressionWrapper(
                    ((((F('not_Prov1')+F('not_Prov1') + F('not_Prov1'))/3) + F('not_examen'))/2),
                    output_field=FloatField()
                ),
                status_prova=Case(
                    When(media_prova__gte=10, then=Value('Apto')),
                    default=Value('N/Apto'),
                    output_field=CharField()
                ),
                status_avaliacao=Case(
                    When(media_avaliacao__gte=10, then=Value('Apto')),
                    default=Value('N/Apto'),
                    output_field=CharField()
                )
            )
        ),
    )

    dados = [{'disciplina': d, 'resultados': d.resultado_set.all() } for d in disciplinas]

    media_prova = 0
    media_avaliacao = 0

    res_valia1 = 'N/Apto'
    res_valia = 'N/Apto'

    for  res in dados:

        if res['resultados']:

            for r  in res['resultados']:

                r.not_Ev_Sist1 = math.ceil(r.not_Ev_Sist1)
                r.not_Ev_Sist2 = math.ceil(r.not_Ev_Sist2)
                r.not_Ev_Sist3 = math.ceil(r.not_Ev_Sist3)

                r.not_Prov1 = math.ceil(r.not_Prov1)
                r.not_Prov2 = math.ceil(r.not_Prov2)
                r.not_Prov3 = math.ceil(r.not_Prov3)
                r.not_examen = math.ceil(r.not_examen)

    context = {
        'dados': dados,
        'media_avaliacao': math.ceil(media_avaliacao),
        'media_prova': math.ceil(media_prova),
        'estudante': estudante,
        'turma': turma,
        'res_valia1': res_valia1,
        'res_valia': res_valia,
        'id_turma': id_turma,
        'id_estudante': id_estudante,
    }

    return render(request, 'lista_turma_estudante/detalhes_turma_estudantes.html', context)

@login_required
def criar_turma(request):

    form = TurmaForm()

    if request.method == 'POST':

        form = TurmaForm(request.POST)

        if form.is_valid():

            turma = form.save()

            context = {
                'sucesso': 'Turma Criada com sucesso!',
                'form': form
            }


            return render(request, 'turma/criar_turma.html', context)
        
        else:
            context = {
                'erro': 'Erro ao ariar a turma, verifique as informações abaixo!',
                'form': form
            }
            return render(request, 'turma/criar_turma.html', context)


    return render(request, 'turma/criar_turma.html', {'form': form})

@login_required
def visualizar_turma(request, id):

    turma = Turma.objects.get(id=id)

    total_estudantes = Matricula.objects.filter(
                turma=turma
            ).count()

    context = {
        'turma': turma,
        'total_estudantes': total_estudantes,
    }

    return render(request, 'turma/visualizar_turma.html', context)

def editar_turma(request, id):

    turma = Turma.objects.get(id=id)

    form = TurmaForm(instance=turma)

    if request.method == 'POST':

        form = TurmaForm(request.POST, instance=turma)

        if form.is_valid():

            turma = form.save()

            context = {
                'sucesso': 'Turma Criada com sucesso!',
                'form': form,
                'turma': turma
            }


            return render(request, 'turma/editar_turma.html', context)
        
        else:
            context = {
                'erro': 'Erro ao ariar a turma, verifique as informações abaixo!',
                'form': form,
                'turma': turma
            }
            return render(request, 'turma/editar_turma.html', context)

    context = {
                'form': form,
                'turma': turma
            }
    return render(request, 'turma/editar_turma.html', context)

@login_required
@require_http_methods('POST')
def delete_turma(request, id):

    turma = Turma.objects.get(id=id)
    
    turma.delete()

    return redirect('listar_turma')

@login_required
def listar_notas(request):

    turmas = Turma.objects.filter(ano_letivo__e_atual=True)
    ano_letivos = AnoLetivo.objects.all()

    per_page = request.GET.get('per_page', 20)
    page = request.GET.get('page', 1)
    order_by = request.GET.get('order_by', 'turma')
    nome_filter = request.GET.get('nome_filter')

    ano_letivo = AnoLetivo.objects.filter(e_atual=True).first()

    if nome_filter:
        ano_letivo = AnoLetivo.objects.get(id=nome_filter)

        nome_filter = nome_filter.strip()

        turmas = ''

        try:
            turmas = Turma.objects.filter(
                ano_letivo=nome_filter
            )

        except Turma.DoesNotExist:

           pass
        

    turmas = turmas.order_by(order_by)

    paginator = Paginator(turmas, per_page)

    obj = paginator.page(page)


    context = {
        'turmas': obj,
        'ano_letivos': ano_letivos,
        'ano_letivo': ano_letivo,
        'order_by': order_by,
        'nome_filter': nome_filter,
        'per_page': per_page
    }
    return render(request, 'notas/listar_notas.html', context)


@login_required
def pauta_turma(request, id_turma):

    turma = Turma.objects.get(id=id_turma)

    id_disciplina = request.GET.get('disPL')

    disciplinas = Disciplina.objects.filter(classe=turma.classe)
    disciplina = Disciplina.objects.filter(classe=turma.classe).first()

    disciplinas_notas = Resultado.objects.filter(
        Q(disciplina = disciplina) &
        Q(turma=turma)
    )

    if id_disciplina:


        disciplinas_notas  = Resultado.objects.filter(
            Q(disciplina = id_disciplina) &
            Q(turma=turma) 
        ).annotate(
            media=ExpressionWrapper(
                (((((F('not_Prov1') + F('not_Prov2') + F('not_Prov3')) / 3) + (F('not_Ev_Sist1') + F('not_Ev_Sist2') + F('not_Ev_Sist3')) / 3)/2) + F('not_examen')) /2,
                output_field=FloatField()
            ),
            status=Case(
                When(media__gte=10, then=Value('Apto')),
                default=Value('N/Apto'),
                output_field=CharField()
            )
            
        )
    else:
        disciplinas_notas = []


    

    for r  in disciplinas_notas:


        r.not_Ev_Sist1 = math.ceil(r.not_Ev_Sist1)
        r.not_Ev_Sist2 = math.ceil(r.not_Ev_Sist2)
        r.not_Ev_Sist3 = math.ceil(r.not_Ev_Sist3)

        r.not_Prov1 = math.ceil(r.not_Prov1)
        r.not_Prov2 = math.ceil(r.not_Prov2)
        r.not_Prov3 = math.ceil(r.not_Prov3)
        r.not_examen = math.ceil(r.not_examen)


    context = {
        'disciplinas_notas': disciplinas_notas,
        'turma': turma,
        'id_turma': id_turma,
        'disciplinas':disciplinas
    }

    return render(request, 'notas/pauta_turma.html', context)


def lista_disciplina(request, id_turma):

    turma = Turma.objects.get(id=id_turma)

    disciplinas = Disciplina.objects.filter(classe=turma.classe)

    per_page = request.GET.get('per_page', 20)
    page = request.GET.get('page', 1)
    order_by = request.GET.get('order_by', 'nome')
    nome_filter = request.GET.get('nome_filter')


    if nome_filter:

        nome_filter = nome_filter.strip()
        disciplinas = disciplinas.filter(
            Q(nome__icontains=nome_filter) |
            Q(abreviatura=nome_filter)
        )

    disciplinas = disciplinas.order_by(order_by)

    paginator = Paginator(disciplinas, per_page)

    obj = paginator.page(page)


    context = {
        'disciplinas': obj,
        'order_by': order_by,
        'nome_filter': nome_filter,
        'per_page': per_page,
        'id_turma': id_turma
    }

    return render(request, 'notas/lista_disciplina.html', context)

@login_required
def adicionar_notas(request, id_turma, id_disciplina):

    turma = Turma.objects.get(id=id_turma)
    disciplina = Disciplina.objects.get(id=id_disciplina)

    estudantes = Matricula.objects.filter(turma=turma)

    forms_list = []

    if request.method == "POST":
        total = int(request.POST.get("total_forms"))

        for i in range(total):
            form = ResultadoForm(request.POST, prefix=f"form-{i}")

            if form.is_valid():
                est_id = form.cleaned_data["estudante_id"]

                resultado, created = Resultado.objects.get_or_create(
                    estudante_id=est_id,
                    turma=turma,
                    disciplina=disciplina,
                    defaults={
                        "not_Ev_Sist1": 0,
                        "not_Ev_Sist2": 0,
                        "not_Ev_Sist3": 0,
                        "not_Prov1": 0,
                        "not_Prov2": 0,
                        "not_Prov3": 0,
                        "not_examen": 0,
                    }
                )

                # Atualiza
                resultado.not_Ev_Sist1 = form.cleaned_data["not_Ev_Sist1"]
                resultado.not_Ev_Sist2 = form.cleaned_data["not_Ev_Sist2"]
                resultado.not_Ev_Sist3 = form.cleaned_data["not_Ev_Sist3"]
                resultado.not_Prov1 = form.cleaned_data["not_Prov1"]
                resultado.not_Prov2 = form.cleaned_data["not_Prov2"]
                resultado.not_Prov3 = form.cleaned_data["not_Prov3"]
                resultado.not_examen = form.cleaned_data["not_examen"]
                resultado.save()

        return redirect(f"adicionar_notas", id_turma=id_turma, id_disciplina=id_disciplina)

    else:
        
        for i, est in enumerate(estudantes):

            try:
                res = Resultado.objects.get(
                    estudante=est.estudante, turma=turma, disciplina=disciplina
                )
                initial = {
                    "estudante_id": est.estudante.id,
                    "not_Ev_Sist1": math.ceil(res.not_Ev_Sist1),
                    "not_Ev_Sist2": math.ceil(res.not_Ev_Sist2),
                    "not_Ev_Sist3": math.ceil(res.not_Ev_Sist3),
                    "not_Prov1": math.ceil(res.not_Prov1),
                    "not_Prov2": math.ceil(res.not_Prov2),
                    "not_Prov3": math.ceil(res.not_Prov3),
                    "not_examen": math.ceil(res.not_examen),
                }
            except Resultado.DoesNotExist:
                initial = {
                    "estudante_id": est.estudante.id,
                    "not_Ev_Sist1": 0,
                    "not_Ev_Sist2": 0,
                    "not_Ev_Sist3": 0,
                    "not_Prov1": 0,
                    "not_Prov2": 0,
                    "not_Prov3": 0,
                    "not_examen": 0,
                }

            form = ResultadoForm(prefix=f"form-{i}", initial=initial)
            forms_list.append({"form": form, "estudante": est.estudante})

    return render(request, "notas/adicionar_notas.html", {
        "forms_list": forms_list,
        "total_forms": len(forms_list),
        "turma": turma,
        "disciplina": disciplina,
    })

@login_required
def criar_usuario(request):

    form = UsuarioForm()

    if request.method == 'POST':

        form = UsuarioForm(request.POST)

        if form.is_valid():

            usuario = form.save()

            
            context = {
                'form': form,
                'sucesso': 'Usuario criado com sucesso!'
            }

            return render(request, 'usuario/criar_usuario.html', context)
        
        else:

            context = {
                'form': form,
                'erro': 'Erro ao criar usuário!'
            }

            return render(request, 'usuario/criar_usuario.html', context)

    else:
        context = {
            'form': form
        }

        return render(request, 'usuario/criar_usuario.html', context)

@login_required
def listar_usuario(request):

    usuarios = Usuario.objects.all()

    per_page = request.POST.get('per_page', 20)
    page = request.POST.get('page', 1)
    nome_filter = request.POST.get('nome_filter')
    ordey_by = request.POST.get('ordey_by')

    paginator = Paginator(usuarios, per_page)

    obj = paginator.page(page)

    context = {
        'usuarios': obj,
        'per_page': per_page,
        'nome_filter': nome_filter,
        'order_by': ordey_by
    }


    return render(request, 'usuario/listar_usuario.html', context)

@login_required
def visualizar_usuario(request, id):

    usuario = Usuario.objects.get(id=id)

    context = {
        'usuario': usuario
    }

    return render(request, 'usuario/visualizar_usuario.html', context)

@login_required
def editar_usuario(request, id):

    usuario = Usuario.objects.get(id=id)

    form = UsuarioForm(instance=usuario)

    if request.method == 'POST':

        form = UsuarioForm(request.POST, instance=usuario)

        if form.is_valid():

            usuario = form.save()

            
            context = {
                'form': form,
                'sucesso': 'Usuário criado com sucesso!',
                'usuario':usuario
            }

            return render(request, 'usuario/editar_usuario.html', context)
        
        else:

            context = {
                'form': form,
                'erro': 'Erro ao criar usuário!',
                'usuario':usuario
            }

            return render(request, 'usuario/editar_usuario.html', context)

    else:
        context = {
            'form': form,
            'usuario':usuario
        }

        return render(request, 'usuario/editar_usuario.html', context)
    

@login_required
def criar_classe(request):

    form = ClasseForm()

    if request.method == 'POST':

        form = ClasseForm(request.POST)

        if form.is_valid():

            classe = form.save()

            
            context = {
                'form': form,
                'sucesso': 'classe criada com sucesso!'
            }

            return render(request, 'classe/criar_classe.html', context)
        
        else:

            context = {
                'form': form,
                'erro': 'Erro ao criar classe!'
            }

            return render(request, 'classe/criar_classe.html', context)

    else:
        context = {
            'form': form
        }

        return render(request, 'classe/criar_classe.html', context)

@login_required
def listar_classe(request):

    classes = Classe.objects.all()

    per_page = request.POST.get('per_page', 20)
    page = request.POST.get('page', 1)
    nome_filter = request.POST.get('nome_filter')
    ordey_by = request.POST.get('ordey_by')

    paginator = Paginator(classes, per_page)

    obj = paginator.page(page)

    context = {
        'classes': obj,
        'per_page': per_page,
        'nome_filter': nome_filter,
        'order_by': ordey_by
    }


    return render(request, 'classe/listar_classe.html', context)

@login_required
def visualizar_classe(request, id):

    classe = Classe.objects.get(id=id)

    try:
        turma = Turma.objects.filter(classe=classe)

    except Turma.DoesNotExist:
        pass

    context = {
        'classe': classe,
        'turma': turma
    }

    return render(request, 'classe/visualizar_classe.html', context)

@login_required
def editar_classe(request, id):

    classe = Classe.objects.get(id=id)

    form = ClasseForm(instance=classe)

    if request.method == 'POST':

        form = ClasseForm(request.POST, instance=classe)

        if form.is_valid():

            classe = form.save()

            
            context = {
                'form': form,
                'sucesso': 'Classe criado com sucesso!',
                'classe':classe
            }

            return render(request, 'classe/editar_classe.html', context)
        
        else:

            context = {
                'form': form,
                'erro': 'Erro ao criar usuário!',
                'classe':classe
            }

            return render(request, 'classe/editar_classe.html', context)

    else:
        context = {
            'form': form,
            'classe':classe
        }

        return render(request, 'classe/editar_classe.html', context)

@login_required
@require_http_methods('POST')
def delete_classe(request, id):

    classe = Classe.objects.get(id=id)
    
    classe.delete()

    return redirect('listar_classe')


@login_required

def configuracao(request):


    form = AnoLetivoForm()

    if request.method == 'POST':
        anos_letivos = AnoLetivo.objects.all()

        form = AnoLetivoForm(request.POST)

        if form.is_valid():

            ano_letivo = form.save()

            
            context = {
                'form': form,
                'anos_letivos': anos_letivos,
                'sucesso': 'Ano letivo criada com sucesso!'
            }

            return render(request, 'configuracao/configuracao.html', context)
        
        else:

            context = {
                'form': form,
                'anos_letivos': anos_letivos,
                'erro': 'Erro ao criar ano letivo!'
            }

            return render(request, 'configuracao/configuracao.html', context)

    else:


        anos_letivos = AnoLetivo.objects.all()

        per_page = request.GET.get('per_page', 20)
        page = request.GET.get('page', 1)

        paginator = Paginator(anos_letivos, per_page)

        obj = paginator.page(page)

        context = {
            'form': form,
            'anos_letivos': obj,
            'page': page,
            'per_page': per_page
        }

        return render(request, 'configuracao/configuracao.html', context)



@login_required
def criar_ano_letivo(request):

    form = AnoLetivoForm()

    if request.method == 'POST':

        form = AnoLetivoForm(request.POST)

        if form.is_valid():

            ano_letivo = form.save()

            
            context = {
                'form': form,
                'sucesso': 'Ano letivo criada com sucesso!'
            }

            return render(request, 'configuracao/configuracao.html', context)
        
        else:

            context = {
                'form': form,
                'erro': 'Erro ao criar ano letivo!'
            }

            return render(request, 'configuracao/configuracao.html', context)

    else:
        context = {
            'form': form
        }

        return render(request, 'configuracao/configuracao.html', context)
    

@login_required
def editar_ano_letivo(request, id):

    ano_letivo = AnoLetivo.objects.get(id=id)

    form = AnoLetivoForm(instance=ano_letivo)

    if request.method == 'POST':

        form = AnoLetivoForm(request.POST, instance=ano_letivo)

        if form.is_valid():

            ano_letivo = form.save()

            
            context = {
                'form': form,
                'sucesso': 'Ano lectivo criado com sucesso!',
                'ano_letivo':ano_letivo
            }

            return render(request, 'configuracao/editar_ano_letivo.html', context)
        
        else:

            context = {
                'form': form,
                'erro': 'Erro ao criar Ano lectivo!',
                'ano_letivo':ano_letivo
            }

            return render(request, 'configuracao/editar_ano_letivo.html', context)

    else:
        context = {
            'form': form,
            'ano_letivo':ano_letivo
        }

        return render(request, 'configuracao/editar_ano_letivo.html', context)


@login_required
def listar_periodo(request):

    periodos = Periodo.objects.all()


    return render(request, 'configuracao/periodo/listar_periodo.html', {'periodos': periodos})

@login_required
def criar_periodo(request):

    if request.method == 'POST':

        periodo = request.POST.get('periodo')

        if not periodo:

            context = {
                'campo': 'campo obrigatório',
                'erro': 'Erro ao salvar período!'
            }

            return render(request, 'configuracao/periodo/criar_periodo.html', context)

        periodo_obj = Periodo(
            periodo = periodo
        )

        periodo_obj.save()

        context = {
                'sucesso': 'Período foi salvo com sucesso!'
            }
        
        return render(request, 'configuracao/periodo/criar_periodo.html', context)
    
    else:

        return render(request, 'configuracao/periodo/criar_periodo.html')

@login_required
def editar_periodo(request, id):

    periodo_obj = Periodo.objects.get(id=id)

    if request.method == 'POST':

        periodo = request.POST.get('periodo')

        if not periodo:

            context = {
                'campo': 'campo obrigatório',
                'erro': 'Erro ao atualizar período!',
                'periodo': periodo_obj
            }

            return render(request, 'configuracao/periodo/editar_periodo.html', context)

        periodo_obj.periodo = periodo

        periodo_obj.save()

        context = {
                'sucesso': 'Período foi alterado com sucesso!',
                'periodo': periodo_obj
            }
        
        return render(request, 'configuracao/periodo/editar_periodo.html', context)
    
    else:

        return render(request, 'configuracao/periodo/editar_periodo.html', {'periodo': periodo_obj})

@login_required
def visualizar_periodo(request, id):

    periodo = Periodo.objects.get(id=id)

    try:
        turma = Turma.objects.filter(periodo=periodo)

    except Turma.DoesNotExist:
        pass


    return render(request, 'configuracao/periodo/visualizar_periodo.html', {'periodo': periodo, 'turma': turma})

@login_required
@require_http_methods('POST')
def delete_periodo(request, id):

    periodo = Periodo.objects.get(id=id)

    periodo.delete()

    return JsonResponse({'sucesso': 'Período Eliminado com sucesso!'}, status=200)

@login_required
def listar_categoria(request):

    categorias = Categoria.objects.all()


    return render(request, 'configuracao/categoria/listar_categoria.html', {'categorias': categorias})

@login_required
def criar_categoria(request):

    if request.method == 'POST':

        categoria = request.POST.get('categoria')

        if not categoria:

            context = {
                'campo': 'campo obrigatório',
                'erro': 'Erro ao salvar Categoria!'
            }

            return render(request, 'configuracao/categoria/criar_categoria.html', context)

        categoria_obj = Categoria(
            categoria = categoria
        )

        categoria_obj.save()

        context = {
                'sucesso': 'Categoria foi salvo com sucesso!'
            }
        
        return render(request, 'configuracao/categoria/criar_categoria.html', context)
    
    else:

        return render(request, 'configuracao/categoria/criar_categoria.html')

@login_required
def editar_categoria(request, id):

    categoria_obj = Categoria.objects.get(id=id)

    if request.method == 'POST':

        categoria = request.POST.get('categoria')

        if not categoria:

            context = {
                'campo': 'campo obrigatório',
                'erro': 'Erro ao atualizar Categoria!',
                'categoria': categoria_obj
            }

            return render(request, 'configuracao/categoria/editar_categoria.html', context)

        categoria_obj.categoria = categoria

        categoria_obj.save()

        context = {
                'sucesso': 'Categoria foi alterada com sucesso!',
                'categoria': categoria_obj
            }
        
        return render(request, 'configuracao/categoria/editar_categoria.html', context)
    
    else:

        return render(request, 'configuracao/categoria/editar_categoria.html', {'categoria': categoria_obj})

@login_required
def visualizar_categoria(request, id):

    categoria = Categoria.objects.get(id=id)

    try:
        professor = Professor.objects.filter(categoria=categoria)

    except Professor.DoesNotExist:
        pass


    return render(request, 'configuracao/categoria/visualizar_categoria.html', {'categoria': categoria, 'professor': professor})

@login_required
@require_http_methods('POST')
def delete_categoria(request, id):

    categoria = Categoria.objects.get(id=id)

    categoria.delete()

    return JsonResponse({'sucesso': 'Categoria Eliminada com sucesso!'}, status=200)

@login_required
def listar_role(request):

    roles = Role.objects.all()


    return render(request, 'configuracao/role/listar_role.html', {'roles': roles})

@login_required
def criar_role(request):

    if request.method == 'POST':

        nome = request.POST.get('nome')

        if not nome:

            context = {
                'campo': 'campo obrigatório',
                'erro': 'Erro ao salvar role!'
            }

            return render(request, 'configuracao/role/criar_role.html', context)

        role_obj = Role(
            nome = nome
        )

        role_obj.save()

        context = {
                'sucesso': 'role foi salva com sucesso!'
            }
        
        return render(request, 'configuracao/role/criar_role.html', context)
    
    else:

        return render(request, 'configuracao/role/criar_role.html')

@login_required
def visualizar_role(request, id):

    role = Role.objects.get(id=id)

    try:
        usuario = Usuario.objects.filter(role=role)

    except Usuario.DoesNotExist:
        pass


    return render(request, 'configuracao/role/visualizar_role.html', {'role': role, 'usuario': usuario})

@login_required
@require_http_methods('POST')
def delete_role(request, id):

    role = Role.objects.get(id=id)

    role.delete()

    return JsonResponse({'sucesso': 'role Eliminada com sucesso!'}, status=200)


@login_required
def listar_horarios(request):
    
    turma_id = request.GET.get('turma')
    ano_letivo_id = request.GET.get('ano_letivo')
    tipo = request.GET.get('tipo')
    
    horarios = HorarioAula.objects.select_related(
        'turma', 'disciplina', 'professor'
    ).all()
    
    if turma_id:
        horarios = horarios.filter(turma_id=turma_id)
    if ano_letivo_id:
        horarios = horarios.filter(ano_letivo_id=ano_letivo_id)
    if tipo:
        horarios = horarios.filter(tipo=tipo)
    
    ordem_dias = {
        'Segunda': 1, 'Terça': 2, 'Quarta': 3, 
        'Quinta': 4, 'Sexta': 5, 'Sábado': 6
    }
    horarios = sorted(horarios, key=lambda x: (
        ordem_dias.get(x.dia_semana, 7), 
        x.hora_inicio
    ))
    
    turmas = Turma.objects.all()
    ano_letivos = AnoLetivo.objects.all()
    tipo_choices = [('prova', 'Prova'), ('aula', 'Aula')]
    
    context = {
        'horarios': horarios,
        'turmas': turmas,
        'ano_letivos': ano_letivos,
        'tipo_choices': tipo_choices,
        'filtros': {
            'turma_id': turma_id,
            'ano_letivo_id': ano_letivo_id,
            'tipo': tipo,
        }
    }
    
    return render(request, 'horario/listar_horarios.html', context)


@login_required
def criar_horario(request):
    if request.method == 'POST':
        form = HorarioAulaForm(request.POST)

        if form.is_valid():

            HorarioAula.objects.create(
                turma=form.cleaned_data['turma'],
                disciplina=form.cleaned_data['disciplina'],
                ano_letivo=form.cleaned_data['ano_letivo'],
                professor=form.cleaned_data['professor'],
                dia_semana=form.cleaned_data['dia_semana'],
                hora_inicio=form.cleaned_data['hora_inicio'],
                hora_fim=form.cleaned_data['hora_fim'],
                tipo=form.cleaned_data['tipo'],
                data_prova=form.cleaned_data['data_prova'],
                sala=form.cleaned_data['sala']
            )
            return redirect('listar_horarios')
    else:
        form = HorarioAulaForm()
    return render(request, 'horario/criar_horario.html', {'form': form, 'action': 'Criar'})

@login_required
def editar_horario(request, id):
    horario = HorarioAula.objects.get(id=id)

    if request.method == 'POST':
        form = HorarioAulaForm(request.POST)
        if form.is_valid():
            horario.turma = form.cleaned_data['turma']
            horario.ano_letivo = form.cleaned_data['ano_letivo']
            horario.disciplina = form.cleaned_data['disciplina']
            horario.professor = form.cleaned_data['professor']
            horario.dia_semana = form.cleaned_data['dia_semana']
            horario.hora_inicio = form.cleaned_data['hora_inicio']
            horario.hora_fim = form.cleaned_data['hora_fim']
            horario.tipo = form.cleaned_data['tipo']
            horario.data_prova = form.cleaned_data['data_prova']
            horario.sala = form.cleaned_data['sala']
            horario.save()
            return redirect('listar_horarios')
    else:

        form = HorarioAulaForm(initial={
            'turma': horario.turma,
            'disciplina': horario.disciplina,
            'professor': horario.professor,
            'dia_semana': horario.dia_semana,
            'hora_inicio': horario.hora_inicio,
            'hora_fim': horario.hora_fim,
            'tipo': horario.tipo,
            'data_prova': horario.data_prova,
            'ano_letivo': horario.ano_letivo,
            'sala': horario.sala
        })

    return render(request, 'horario/editar_horario.html', {'form': form, 'action': 'Editar'})

@login_required
@require_http_methods('POST')
def delete_horario(request, id):

    horario = HorarioAula.objects.get(id=id)

    horario.delete()

    return redirect('listar_horarios')


@login_required
def gerar_certificado(request, estudante_id):

    estudante = get_object_or_404(Estudante, id=estudante_id)
    
    resultados = Resultado.objects.filter(estudante=estudante).select_related(
        'disciplina', 'turma'
    )
    
    if not resultados.exists():
        return HttpResponse("Não há resultados registrados para este estudante.", status=404)
    
    disciplinas_aprovadas = []
    media_geral = 0
    
    for resultado in resultados:

        media_sistema = (
            resultado.not_Ev_Sist1 + 
            resultado.not_Ev_Sist2 + 
            resultado.not_Ev_Sist3
        ) / 3
        
        media_provas = (
            resultado.not_Prov1 + 
            resultado.not_Prov2 + 
            resultado.not_Prov3
        ) / 3
        
        media_final = (math.ceil(media_sistema) * 0.4) + (math.ceil(media_provas) * 0.6)
        
        if media_final < 10: 
            media_final = (media_final + resultado.not_examen) / 2

        extenso = ''
        num = ['um', 'dois', 'três','quatro', 'cinco', 'seis','sete', 'oito', 'nove','dez', 'onze', 'doze','treze', 'catorze', 'quinze', 'dezaseis', 'dezassete', 'dezoito', 'dezanove', 'vinte']
        for i,v in enumerate(num):
            if round(media_final) == i+1:
                extenso = v

                break
        
        disciplinas_aprovadas.append({
            'nome': resultado.disciplina.nome,
            'media': round(media_final),
            'aprovado': media_final >= 10,
            'extenso': extenso
        })
        
        media_geral += media_final
    
    media_geral = round(media_geral / len(disciplinas_aprovadas))
    
    aprovado_geral = all(d['aprovado'] for d in disciplinas_aprovadas)
    
    turma = resultados.first().turma

    imagem_caminho = os.path.join(settings.STATICFILES_DIRS[0], "image/Insignia.png")
    with open(imagem_caminho, "rb") as f:
        imagem_base64 = base64.b64encode(f.read()).decode()
    
    data = datetime.now().strftime('%d-%m-%Y')
    context = {
        'estudante': estudante,
        'turma': turma,
        'disciplinas': disciplinas_aprovadas,
        'media_geral': media_geral,
        'aprovado': aprovado_geral,
        'total_disciplinas': len(disciplinas_aprovadas),
        'logo_base64': imagem_base64,
        'hoje': data
    }
    
    html = render(request, 'notas/certificado.html', context).content.decode('utf-8')
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=estudantes_{datetime.now().strftime("%Y%m%d")}.pdf'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=400)
    
    return response


@login_required
def listar_estudantes_certificado(request):
  
    # Buscar estudantes com resultados
    estudantes_com_resultados = Estudante.objects.filter(
        resultado__isnull=False
    ).distinct()
    
    context = {
        'estudantes': estudantes_com_resultados
    }
    
    return render(request, 'notas/listar_certificados.html', context)