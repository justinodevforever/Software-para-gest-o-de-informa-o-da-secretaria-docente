from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.dashboard_estatisticas, name='dashboard'),
    
    path('relatorio/estudantes/', views.relatorio_estudantes, name='relatorio_estudantes'),
    path('relatorio/estudantes/excel/', views.relatorio_estudantes_excel, name='estudantes_excel'),
    path('relatorio/estudantes/pdf/', views.relatorio_estudantes_pdf, name='estudantes_pdf'),
    
    path('relatorio/notas/', views.relatorio_notas, name='notas'),
    path('relatorio/notas/excel/', views.relatorio_notas_excel, name='notas_excel'),
    
    path('relatorio/professores/', views.relatorio_professores, name='professores'),
    
    path('relatorio/turmas/', views.relatorio_turmas, name='turmas'),
]