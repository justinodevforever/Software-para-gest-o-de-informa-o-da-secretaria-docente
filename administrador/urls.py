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

]