from django.urls import path
from .views import *



urlpatterns = [
    path('', index, name='index'),
    path('lista_professor/', lista_professor, name='lista_professor'),
    path('criar_professor/', criar_professor, name='criar_professor'),
    path('editar_professor/<int:id>/', editar_professor, name='editar_professor'),
    path('visualizar_professor/<int:id>/', visualizar_professor, name='visualizar_professor'),
    path('delete_professor/<int:id>/', delete_professor, name='delete_professor'),

    path('lista_estudante/', lista_estudante, name='lista_estudante'),
    path('editar_estudante/<int:id>/', editar_estudante, name='editar_estudante'),
    path('visualizar_estudante/<int:id>/', visualizar_estudante, name='visualizar_estudante'),

    path('criar_matricula/', criar_matricula, name='criar_matricula'),
    path('lista_matricula/', lista_matricula, name='lista_matricula'),
    path('visualizar_matricula/<int:id>/', visualizar_matricula, name='visualizar_matricula'),
    path('editar_matricula/<int:id>/', editar_matricula, name='editar_matricula'),

    path('listar_disciplina/', listar_disciplina, name='listar_disciplina'),
    path('criar_disciplina/', criar_disciplina, name='criar_disciplina'),
    path('visualizar_disciplina/<int:id>/', visualizar_disciplina, name='visualizar_disciplina'),
    path('editar_disciplina/<int:id>/', editar_disciplina, name='editar_disciplina'),
    path('delete_disciplina/<int:id>/', delete_disciplina, name='delete_disciplina'),
    
    path('listar_turma/', listar_turma, name='listar_turma'),
    path('criar_turma/', criar_turma, name='criar_turma'),
    path('visualizar_turma/<int:id>/', visualizar_turma, name='visualizar_turma'),
    path('editar_turma/<int:id>/', editar_turma, name='editar_turma'),
    path('delete_turma/<int:id>/', delete_turma, name='delete_turma'),

    path('listar_turma_estudantes/<int:id_turma>/', listar_turma_estudantes, name='listar_turma_estudantes'),
    path('detalhes_turma_estudantes/<int:id_estudante>/<int:id_turma>/', detalhes_turma_estudantes, name='detalhes_turma_estudantes'),

    path('listar_notas/', listar_notas, name='listar_notas'),
    path('pauta_turma/<int:id_turma>/', pauta_turma, name='pauta_turma'),
    path('lista_disciplina/<int:id_turma>/', lista_disciplina, name='lista_disciplina'),
    path('adicionar_notas/<int:id_turma>/<int:id_disciplina>/', adicionar_notas, name='adicionar_notas'),

    path('criar_usuario/', criar_usuario, name='criar_usuario'),
    path('listar_usuario/', listar_usuario, name='listar_usuario'),
    path('visualizar_usuario/<int:id>/', visualizar_usuario, name='visualizar_usuario'),
    path('editar_usuario/<int:id>/', editar_usuario, name='editar_usuario'),

    path('criar_classe/', criar_classe, name='criar_classe'),
    path('listar_classe/', listar_classe, name='listar_classe'),
    path('editar_classe/<int:id>/', editar_classe, name='editar_classe'),
    path('visualizar_classe/<int:id>/', visualizar_classe, name='visualizar_classe'),
    path('delete_classe/<int:id>/', delete_classe, name='delete_classe'),

    path('configuracao/', configuracao, name='configuracao'),
    path('criar_ano_letivo/', criar_ano_letivo, name='criar_ano_letivo'),
    path('editar_ano_letivo/<int:id>/', editar_ano_letivo, name='editar_ano_letivo'),

    path('listar_periodo/', listar_periodo, name='listar_periodo'),
    path('criar_periodo/', criar_periodo, name='criar_periodo'),
    path('visualizar_periodo/<int:id>/', visualizar_periodo, name='visualizar_periodo'),
    path('editar_periodo/<int:id>/', editar_periodo, name='editar_periodo'),
    path('delete_periodo/<int:id>/', delete_periodo, name='delete_periodo'),

    path('listar_categoria/', listar_categoria, name='listar_categoria'),
    path('criar_categoria/', criar_categoria, name='criar_categoria'),
    path('visualizar_categoria/<int:id>/', visualizar_categoria, name='visualizar_categoria'),
    path('editar_categoria/<int:id>/', editar_categoria, name='editar_categoria'),
    path('delete_categoria/<int:id>/', delete_categoria, name='delete_categoria'),

    path('listar_role/', listar_role, name='listar_role'),
    path('criar_role/', criar_role, name='criar_role'),
    path('visualizar_role/<int:id>/', visualizar_role, name='visualizar_role'),
    path('delete_role/<int:id>/', delete_role, name='delete_role'),

    path('listar_horarios/', listar_horarios, name='listar_horarios'),
    path('criar_horario/', criar_horario, name='criar_horario'),
    path('editar_horario/<int:id>/', editar_horario, name='editar_horario'),
    path('delete_horario/<int:id>/', delete_horario, name='delete_horario'),

    path('certificados/', listar_estudantes_certificado, name='lista_certificados'),
    
    path('certificados/<int:estudante_id>/', gerar_certificado, name='gerar_certificado'),

    path('reconfirmacao/', reconfirmacao, name='reconfirmacao'),

]