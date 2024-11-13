from django.contrib import admin
from django.urls import path
from appCampanha import views
from projetoCampanha import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.home, name="home"),
    path("calendario/", views.calendario, name="calendario"),
    path("marcar_calendario/", views.marcar_calendario, name="marcar_calendario"),
     path("calendario_resumo/", views.calendario_resumo, name="calendario_resumo"),
    path('buscar-nome-por-cpf/', views.buscar_nome_por_cpf, name='buscar_nome_por_cpf'),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("chamar_senha/", views.chamar_senha, name="chamar_senha"),
    path("ultimas_senhas/", views.ultimas_senhas, name="ultimas_senhas"),
    path("ultimas_senhas_json/", views.ultimas_senhas_json, name="ultimas_senhas_json"),
    path("criar_senha/", views.criar_senha, name="criar_senha"),
    path('apagar-senhas/', views.apagar_senhas, name='apagar_senhas'),
    path("relatorio_senhas/", views.relatorioSenha, name="relatorio_senhas"),

    path("cadastro/", views.cadastro, name="cadastro"),
    path("cadastro2", views.cadastro2, name="cadastro2"),
    path('eleitor/<int:eleitor_id>/adicionar_endereco/', views.adicionar_endereco, name='adicionar_endereco'),
    path('editar_eleitor/<int:usuario_id>', views.editar_eleitor, name='editar_eleitor'),
    path('editar-endereco/<int:endereco_id>/', views.editar_endereco, name='editar_endereco'),
    path('excluir-endereco/<int:endereco_id>/', views.excluir_endereco, name='excluir_endereco'),
    path("apagar_eleitor/<int:usuario_id>", views.apagarEleitor, name="apagar_eleitor"),
    path("confirm_eleitor/<int:usuario_id>", views.confirm_eleitor, name="confirm_eleitor"),
    path("eleitores/", views.eleitores, name="eleitores"),

    path("assunto_inserir/<int:usuario_id>", views.assunto_inserir, name="assunto_inserir"),
    path("post_assunto/", views.post_assunto, name="post_assunto"),
    path("assunto_sucesso/", views.assunto_sucesso, name="assunto_sucesso"),
    path("assuntos/", views.assuntos, name="assuntos"),
    path('assuntos/atendimento/<int:assunto_id>/', views.gerenciar_atendimento, name='gerenciar_atendimento'),
    path('assuntos/finalizar/<int:assunto_id>/', views.finalizar_atendimento, name='finalizar_atendimento'),
    path('assuntos/detalhes/<int:assunto_id>/', views.assunto_detalhes, name='assunto_detalhes'),
    path("apagar_assunto/<int:assunto_id>", views.apagarAssunto, name="apagar_assunto"),
    path("confirm_assunto/<int:assunto_id>", views.confirm_assunto, name="confirm_assunto"),

    path("tabela_eleitor/", views.tabela_eleitor, name="tabela_eleitor"),
    path("relatorio_eleitor/<int:usuario_id>", views.relatorio_eleitor, name="relatorio_eleitor"),

    path("tabela_usuario", views.tabela_usuario, name="tabela_usuario"),
    path("relatorio_usuario/<int:user_id>", views.relatorio_usuario, name="relatorio_usuario"),


    path("login/", views.login, name="login"),
    path("login-eleitor/", views.login_eleitor, name="login_eleitor"),
    path('assuntos-eleitor/<int:usuario_id>/<str:cpf>/', views.assuntos_eleitor, name='assuntos_eleitor'),
    path('privacidade', views.privacidade, name='privacidade'),

    path("perfil/", views.edit_profile, name="edit_profile"),
    path("alterar_senha/", views.alterar_senha, name="alterar_senha"),
    path("novo_acesso/", views.novo_acesso, name="novo_acesso"),
    path("sair/", views.sair, name="sair"),


    path('api/get-data/<int:period>/', views.get_data, name='get_data'),
    path('notificacoes/', views.all_notifications, name='notificacoes'),
    path('send-notification/', views.send_notification, name='send_notification'),
    path('notifications/get/', views.get_notifications, name='get_notifications'),
    path('notifications/unread_count/', views.unread_notifications_count, name='unread_notifications_count'),
    path('notifications/mark_all_as_read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('mark-notification-as-read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
