from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

from .models import *
from .forms import *

@login_required
def index(request):

    return render(request, 'index.html')

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


    return render(request, 'estudante/visualizar_estudante.html', {'estudante': estudante})


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