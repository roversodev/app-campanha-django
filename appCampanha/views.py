from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from requests import request
from appCampanha.forms import LoginForm
from projetoCampanha import settings
from .models import Eleitor, Assunto, Endereco, Observacao, Dataretorno, Senha, CustomUser, Atuacao
import time
import re
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging
from ipware.ip import get_client_ip
from datetime import datetime, timedelta
from django.contrib.auth import logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from rolepermissions.decorators import has_permission_decorator
from django.utils import timezone
from django.utils.timezone import now
from django.contrib import messages
from django.db.models import F, ExpressionWrapper, DurationField, Avg, Count, Q
from django.db.models.functions import TruncDate, TruncHour
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import IntegrityError
from notifications.signals import notify
import json
from notifications.models import Notification
from django.utils.timesince import timesince
from rolepermissions.roles import get_user_roles


logger = logging.getLogger('user')
loggerINFO = logging.getLogger('django')


# FUNÇÕES ------------------

def extrair_nome_receita(cpf, data_nascimento):

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Abrir a página
    driver.get("https://servicos.receita.fazenda.gov.br/Servicos/CPF/ConsultaSituacao/ConsultaPublica.asp")

    # Preencher o campo CPF
    time.sleep(1)
    cpf_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "txtCPF"))
    )
    cpf_input.send_keys(cpf)

    time.sleep(1)

    # Preencher o campo data de nascimento
    data_nascimento_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "txtDataNascimento"))
    )
    data_nascimento_input.send_keys(data_nascimento)

    time.sleep(2)

    driver.switch_to.active_element.send_keys(Keys.TAB)

    time.sleep(1)

    elemento_com_foco = driver.switch_to.active_element

    elemento_com_foco.send_keys(Keys.SPACE)

    elemento_com_foco.click()


    time.sleep(1)

    # Clicar no botão "Consultar" (opcional)
    consultar_button = driver.find_element(By.NAME, "Enviar")
    consultar_button.click()

    time.sleep(1)

    # Extrair o nome completo da página de resultados
    try:
            # Encontra o elemento com a classe 'clConteudoEsquerda'
            conteudo_esquerda = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "clConteudoEsquerda"))
            )

            # Extrai o texto do elemento e usa regex para encontrar o nome
            texto_conteudo = conteudo_esquerda.text
            padrao_nome = r"Nome:\s*(.*)"
            correspondencia = re.search(padrao_nome, texto_conteudo)

            if correspondencia:
                nome_completo = correspondencia.group(1).strip()
                driver.quit()  # Fechar o navegador após obter o nome
                return nome_completo
            else:
                logger.critical("Erro ao Consultar na Receita!")
                raise Exception("Nome não encontrado no conteúdo da página.")

    except Exception as e:
            logger.critical("Erro ao Consultar na Receita!")
            driver.quit()
            print(f"Erro ao extrair o nome completo: {e}")
            return None




def notificar_atendente():
    autor = CustomUser.objects.get(id=1)
    now_utc = timezone.now()  # Hora atual
    now = timezone.localtime(now_utc)

    # Notificação para o dia exato (à meia-noite do dia)
    data_notificacao_dia = now.date()

    # Notificação faltando 30 minutos para o evento
    intervalo_30_min = now + timedelta(minutes=30)

    # Buscando eventos no dia atual
    eventos_hoje = Dataretorno.objects.filter(data=data_notificacao_dia)

    for evento in eventos_hoje:
        hora_formatada = evento.hora.strftime("%H:%M")
        # Notificação do dia, se ainda não foi enviada
        if not evento.notificacao_enviada_dia and evento.hora <= intervalo_30_min.time():
            notify.send(
                autor,
                recipient=evento.atendente,
                verb=f"Você tem um compromisso agendado com CPF: {evento.cliente.cpf} às {hora_formatada}."
            )
            evento.notificacao_enviada_dia = True
            evento.save()

    # Buscar eventos nos próximos 30 minutos
    eventos_30_min = Dataretorno.objects.filter(
        data=data_notificacao_dia,
        hora__gte=now.time(),
        hora__lte=intervalo_30_min
    )

    for evento in eventos_30_min:
        hora_formatada = evento.hora.strftime("%H:%M")
        # Notificação de 30 minutos antes, se ainda não foi enviada
        if not evento.notificacao_enviada_30min:
            notify.send(
                autor,
                recipient=evento.atendente,
                verb=f"Faltam menos de 30 minutos para o compromisso com CPF: {evento.cliente.cpf}, às {hora_formatada}."
            )
            evento.notificacao_enviada_30min = True
            evento.save()



def notificar_role(verb, sender, role_name):
    users = CustomUser.objects.filter(is_superuser=False)

    for user in users:
        roles = get_user_roles(user)
        if any(role.__name__ == role_name for role in roles):
            notify.send(sender, recipient=user, verb=verb)



@login_required
def send_notification(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        recipients_ids = data.get('recipients', [])
        message = data.get('message', '')

        if recipients_ids and message:
            recipients = CustomUser.objects.filter(id__in=recipients_ids)
            for recipient in recipients:
                notify.send(
                    sender=request.user,
                    recipient=recipient,
                    verb=message
                )

            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Dados inválidos'}, status=400)



def get_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user, unread=True)
    data = []

    for notification in notifications:
        data.append({
            'id': notification.id,
            'verb': notification.verb,
            'unread': notification.unread,
            'timestamp_timesince': timesince(notification.timestamp),
            'sender': notification.actor.username if notification.actor else "Desconhecido"
        })

    return JsonResponse({'notifications': data})



def mark_notification_as_read(request, notification_id):
    if request.method == 'POST':
        notification = Notification.objects.get(id=notification_id)
        notification.mark_as_read()  # Marque como lida
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)




def unread_notifications_count(request):
    if request.user.is_authenticated:
        unread_count = request.user.notifications.unread().count()
        return JsonResponse({'unread_count': unread_count})
    return JsonResponse({'unread_count': 0})



@login_required
def mark_all_as_read(request):
    if request.method == 'POST':

        notifications = Notification.objects.filter(recipient=request.user, unread=True)
        notifications.update(unread=False)
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'fail'}, status=400)



@login_required
def all_notifications(request):
    if request.user.is_authenticated:
        notifications = request.user.notifications.all()

        for notification in notifications:
            notification.sender = notification.actor
        
        users = CustomUser.objects.all()

        return render(request, 'all_notifications.html', {'notifications': notifications, 'users': users})




def valida_cpf(cpf):
    # Remove caracteres não numéricos
    cpf = cpf.replace('.', '').replace('-', '')
    cpf = ''.join(i for i in cpf if i.isdigit())

    # Verifica se o CPF possui 11 dígitos
    if len(cpf) != 11:
        return False

    # Se todos os dígitos forem iguais, o CPF é inválido
    if cpf == '00000000000' or cpf == '11111111111' or cpf == '22222222222' or cpf == '33333333333' or cpf == '44444444444' or cpf == '55555555555' or cpf == '66666666666' or cpf == '77777777777' or cpf == '88888888888' or cpf == '99999999999':
        return False

    # Cálculo dos dígitos verificadores
    novo_cpf = cpf[:9]
    reverso = 10
    total = 0

    for x in range(9):
        total += int(novo_cpf[x]) * reverso
        reverso -= 1
        if reverso < 2:
            reverso = 11
    resto = total % 11
    if resto < 2:
        digito1 = 0
    else:
        digito1 = 11 - resto

    novo_cpf += str(digito1)
    total = 0
    reverso = 11
    for x in range(10):
        total += int(novo_cpf[x]) * reverso
        reverso -= 1
    resto = total % 11
    if resto < 2:
        digito2 = 0
    else:
        digito2 = 11 - resto

    dg = str(digito1) + str(digito2)

    if dg == cpf[9:11]:
        return True
    else:
        return True
    



def ultimas_senhas(request):
    ultimas_senhas = Senha.objects.filter(atendida=True).order_by('-chamada')[:4]
    senhas_chamadas = Senha.objects.filter(atendida=True)
    context = {
        'ultimas_senhas': ultimas_senhas,
    }
    return render(request, 'ultimas_senhas.html', context)




def criar_senha(request):
    if request.method == 'POST':

        ultima_senha = Senha.objects.order_by('numero').last()
        proximo_numero = ultima_senha.numero + 1 if ultima_senha else 1
        
        nova_senha = Senha.objects.create(numero=proximo_numero)

        return JsonResponse({'numero': nova_senha.numero})
    
    return render(request, 'criar_senha.html')




@login_required
@has_permission_decorator('sprusr')
def apagar_senhas(request):
    Senha.objects.all().delete()
    messages.success(request, 'Todas as senhas foram apagadas com sucesso.')
    user = CustomUser.objects.get(pk=request.user.id)
    extra = {
            'user_id': user.id,
            'username': user.username,
            'ip_address': request.META.get('REMOTE_ADDR')
                }    
    logger.warning('APAGOU todas as SENHAS do sistema.', extra=extra)
    return redirect('relatorio_senhas')




@login_required
def chamar_senha(request):
    # Obtém a próxima senha disponível (não atendida)
    proxima_senha = Senha.objects.filter(atendida=False).order_by('numero').first()

    if proxima_senha:
        proxima_senha.atendida = True
        proxima_senha.chamada = timezone.now()
        proxima_senha.atendente = request.user
        proxima_senha.save()
        user = CustomUser.objects.get(pk=request.user.id)
        extra = {
                'user_id': user.id,
                'username': user.username,
                'ip_address': request.META.get('REMOTE_ADDR')
                    }    
        logger.warning('Chamou a senha: %s', proxima_senha.numero,extra=extra)

        return JsonResponse({'numero': proxima_senha.numero})
    
    return JsonResponse({'erro': 'Nenhuma senha disponível'})




def ultimas_senhas_json(request):
    senhas = (Senha.objects.filter(atendida=True)
              .order_by('-chamada')[:4]
              .select_related('atendente'))
    data = [{
        'numero': senha.numero,
        'atendente': senha.atendente.username if senha.atendente else 'N/A'} for senha in senhas]
    return JsonResponse(data, safe=False)



@login_required
@has_permission_decorator('staff')
def relatorioSenha(request):
    total_senhas = Senha.objects.count()
    total_atendidas = Senha.objects.filter(atendida=True).count()
    total_pendentes = Senha.objects.filter(atendida=False).count()
    desempenho = (
    CustomUser.objects.annotate(
        senha_count=Count('senha', filter=Q(senha__atendida=True)),
        tempo_medio_espera=Avg(
            ExpressionWrapper(F('senha__chamada') - F('senha__data_criacao'), output_field=DurationField()),
            filter=Q(senha__atendida=True)
        )
    )
    .values('username', 'senha_count', 'tempo_medio_espera')
)
    
    for user in desempenho:
        tempo = user['tempo_medio_espera']
        if tempo:
            total_seconds = int(tempo.total_seconds())
            horas, resto = divmod(total_seconds, 3600)
            minutos, segundos = divmod(resto, 60)
            user['tempo_medio_espera_formatado'] = f"{horas:02}:{minutos:02}:{segundos:02}"
        else:
            user['tempo_medio_espera_formatado'] = "00:00:00"
    
    # Cálculo do tempo médio
    queryset = Senha.objects.filter(atendida=True).annotate(
        tempo_espera=ExpressionWrapper(
            F('chamada') - F('data_criacao'),
            output_field=DurationField()
        )
    )
    tempo_medio = queryset.aggregate(Avg('tempo_espera'))['tempo_espera__avg']
    tempo_medio_str = str(tempo_medio).split('.')[0] if tempo_medio is not None else '0'

    
    # Últimas senhas atendidas
    hoje1 = timezone.now().date()
    ultimas_senhas = Senha.objects.filter(data_criacao__date=hoje1).order_by('-data_criacao')


    hoje = timezone.now()
    dias = [hoje - timedelta(days=i) for i in range(30)]  # últimos 30 dias
    senhas_por_dia = Senha.objects.filter(atendida=True, data_criacao__date__in=[dia.date() for dia in dias]) \
        .annotate(data=TruncDate('data_criacao')) \
        .values('data') \
        .annotate(total=Count('id')) \
        .order_by('data')

    labels = [dia.strftime('%d/%m') for dia in dias]
    data = [0] * 30

    for senha in senhas_por_dia:
        index = (hoje.date() - senha['data']).days
        if 0 <= index < 30:
            data[index] = senha['total']

    # Gráfico de Distribuição de Senhas por Hora
    horas = (
    Senha.objects.filter(atendida=True, chamada__date=hoje)
    .annotate(hora=TruncHour('chamada'))
    .values('hora')
    .annotate(total=Count('id'))
    .order_by('hora')
    )

    # Formata os dados para o gráfico
    labels_horas = [senha['hora'].strftime('%H:%M') for senha in horas]
    data_horas = [senha['total'] for senha in horas]
    
    context = {
        'total_senhas': total_senhas,
        'total_atendidas': total_atendidas,
        'total_pendentes': total_pendentes,
        'tempo_medio': tempo_medio_str,
        'ultimas_senhas': ultimas_senhas,
        'labels': labels,
        'data': data,
        'labels_horas': labels_horas,
        'data_horas': data_horas,
        'desempenho': desempenho,
    }

    user = CustomUser.objects.get(pk=request.user.id)
    extra = {
            'user_id': user.id,
            'username': user.username,
            'ip_address': request.META.get('REMOTE_ADDR')
                }    
    logger.warning('Acessou o RELATÓRIO DE SENHAS.', extra=extra)
    
    return render(request, 'relatorio_senhas.html', context)




# LOGIN E SENHA ------------------
def login(request):
    if request.method == 'GET':
        extra = {
            'user_id': None,
            'username': None,
            'ip_address': request.META.get('REMOTE_ADDR')
        }
        logger.info('Acessou a pagina de LOGIN.', extra=extra)
        return render(request, "login.html", {
            'form': AuthenticationForm
        })
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            extra = {
                'user_id': user.id,
                'username': user.username,
                'ip_address': request.META.get('REMOTE_ADDR')
            }
            logger.info('Usuario logado.', extra=extra)

            # Verifica se é o primeiro login
            if user.is_first_login:
                adm = CustomUser.objects.get(id=1)
                notify.send(sender=adm, recipient=user, verb='Bem-vindo ao nosso Sistema!')
                notify.send(sender=adm, recipient=user, verb='Para marcar como lida basta clicar em cima da notificação!')
                user.is_first_login = False
                user.save()

            # Redirecionar para o próximo URL, se houver, caso contrário, para a home
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')
        else:
            extra = {
                'user_id': None,
                'username': username,
                'ip_address': request.META.get('REMOTE_ADDR')
            }
            logger.warning('Tentou Logar com Usuario ou senha inválida', extra=extra)
            return render(request, 'login.html', {'form': AuthenticationForm, 'error': 'Usuário ou Senha inválidos'})




def login_eleitor(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf']
            dataN = form.cleaned_data['dataN']

            try:
                usuario = Eleitor.objects.get(cpf=cpf, dataN=dataN)

                cpf_certo = desmascarar_cpf(usuario.cpf)

                extra = {
                    'user_id': "Null",
                    'username': "Null",
                    'ip_address': request.META.get('REMOTE_ADDR')
                }    
                logger.warning('Acessou a Pagina de LOGIN - ELEITOR', extra=extra)
                # Redirecionar para a página de assuntos do usuário
                return redirect('assuntos_eleitor', usuario_id=usuario.id_usuario, cpf=cpf_certo)
            except Eleitor.DoesNotExist:
                return render(request, 'login_eleitor.html', {'form': form, 'error': 'CPF ou Data de Nascimento inválida.'})
    else:
        form = LoginForm()

    return render(request, 'login_eleitor.html', {'form': form})



def assuntos_eleitor(request, usuario_id, cpf):
    # Lógica para buscar os assuntos do usuário
    usuarios = Eleitor.objects.get(id_usuario=usuario_id)
    assuntos = Assunto.objects.filter(clienteEscolhido=usuarios).order_by('-data_criacao')

    extra = {
                    'user_id': "Null",
                    'username': "Null",
                    'ip_address': request.META.get('REMOTE_ADDR')
                }    
    logger.warning('Acessou a Pagina de VERIFICAÇÃO DE ASSUNTOS - ELEITOR ELEITOR ID:%s', usuarios.id_usuario,extra=extra)

    return render(request, 'assuntos_eleitor.html', {'assuntos': assuntos})



def privacidade(request):
    return render(request, 'politica_privacidade.html')




def desmascarar_cpf(cpf):
    return re.sub(r'\D', '', cpf)



@login_required
def sair(request):
    user = CustomUser.objects.get(pk=request.user.id)
    extra = {
            'user_id': user.id,
            'username': user.username,
            'ip_address': request.META.get('REMOTE_ADDR')
            }    
    logger.info('Usuário logout.', extra=extra)
    logout(request)
    return redirect('login')



@login_required
def alterar_senha(request):
    if request.method == "POST":
        form_senha = PasswordChangeForm(request.user, request.POST)
        if form_senha.is_valid():
            user = form_senha.save()
            update_session_auth_hash(request, user)
            user = CustomUser.objects.get(pk=request.user.id)
            extra = {
            'user_id': user.id,
            'username': user.username,
            'ip_address': request.META.get('REMOTE_ADDR')
            }    
            logger.warning('Usuário alterou a Senha.', extra=extra)
            return render(request, 'senha_alterada.html')
    else:
        user = CustomUser.objects.get(pk=request.user.id)
        extra = {
                'user_id': user.id,
                'username': user.username,
                'ip_address': request.META.get('REMOTE_ADDR')
                    }    
        logger.info('Acessou a pagina de ALTERAR SENHA', extra=extra)
        form_senha = PasswordChangeForm(request.user)
    return render(request, 'alterar_senha.html', {'form_senha': form_senha})



@login_required
@has_permission_decorator('staff')
def novo_acesso(request):
    if request.method == 'GET':
        atuacoes = Atuacao.objects.all()
        return render(request, 'novo_acesso.html', {
            'form': UserCreationForm,
            'atuacoes': atuacoes,
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Captura os dados do formulário
                username = request.POST['username']
                password = request.POST['password1']
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                email = request.POST['email']
                
                # Tenta criar o usuário, e captura exceção se o usuário já existir
                user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                
                # Verifica a função e atribui o papel correspondente
                if request.POST.get('funcao') == 'Frente':
                    assign_role(user, 'frente')
                elif request.POST.get('funcao') == 'Solucionador':
                    assign_role(user, 'solucionador')
                elif request.POST.get('funcao') == 'Atendente':
                    assign_role(user, 'atendente')
                elif request.POST.get('funcao') == 'Staff':
                    assign_role(user, 'staff')

                atuacoes_ids = request.POST.getlist('atuacoes')  # 'atuacoes' é o nome do campo
                for atuacao_id in atuacoes_ids:
                    atuacao = Atuacao.objects.get(id=atuacao_id)
                    user.atuacoes.add(atuacao)

                user.save()  # Salva o usuário com as atuações atribuídas
                
                # Log do sucesso
                extra = {
                    'user_id': user.id,
                    'username': user.username,
                    'ip_address': request.META.get('REMOTE_ADDR')
                }
                logger.warning('Novo acesso criado com sucesso Acesso: %s', username, extra=extra)
                
                return render(request, 'novo_acesso_confirm.html')
            
            # Captura erro de integridade (usuário já existe)
            except IntegrityError:
                logger.error('Tentativa de criar um usuário existente: %s', username)
                return render(request, 'novo_acesso.html', {
                    'form': UserCreationForm, 
                    "error": 'Usuário já existe!'
                })
        else:
            return render(request, 'novo_acesso.html', {
                'form': UserCreationForm,
                "error": 'Senhas são diferentes.'
            })




# SITE ------------------
@login_required
@has_permission_decorator('home')
def home(request):

    if has_role(request.user, 'frente') and not request.user.is_superuser:
        return redirect('/cadastro')
    

    notificar_atendente()
    
    hoje = datetime.today().date()
    agendamentos_futuros = Dataretorno.objects.filter(data__gte=hoje).order_by('data')
    agendamentos_futuros_limitados = agendamentos_futuros[:5]
    eleitores = Eleitor.objects.order_by('-data_criacao')[:5]

    data_limite = now() - timedelta(days=7)

    # Contar registros das tabelas Eleitor, Assunto, Solucao e Dataretorno
    total_eleitores = Eleitor.objects.filter(data_criacao__gte=data_limite).count()
    total_assuntos = Assunto.objects.filter(data_criacao__gte=data_limite).count()
    total_solucoes = Assunto.objects.filter(data_finalizacao__gte=data_limite, solucionado__in=['Solucionado', 'Parcialmente Solucionado']).count()
    total_dataretornos = agendamentos_futuros_limitados.count()

    context = {
        'total_eleitores': total_eleitores,
        'total_assuntos': total_assuntos,
        'total_solucoes': total_solucoes,
        'total_dataretornos': total_dataretornos,
        'agendamentos_hoje': agendamentos_futuros_limitados,
        'eleitores': eleitores,
    }
        
    client_ip, is_routable = get_client_ip(request)
    user = CustomUser.objects.get(pk=request.user.id)
    extra = {
        'user_id': user.id,
        'username': user.username,
        'ip_address': client_ip
    }    
    logger.info('Acessou a HOME.', extra=extra)
    return render(request, "home.html", context)




@login_required
@has_permission_decorator('calendario')
def calendario(request):
    if request.method == 'GET':
            
            user = CustomUser.objects.get(pk=request.user.id)
            extra = {
            'user_id': user.id,
            'username': user.username,
            'ip_address': request.META.get('REMOTE_ADDR')
            }    
            logger.info('Acessou o CALENDARIO.', extra=extra)

            dataretornos = {
                'dataretornos': Dataretorno.objects.all()
            }
            return render(request, "calendario.html", dataretornos)
    else:
        user = CustomUser.objects.get(pk=request.user.id)
        extra = {
            'user_id': user.id,
            'username': user.username,
            'ip_address': request.META.get('REMOTE_ADDR')
            }    
        logger.warning('Marcou um Eleitor no Calendario.', extra=extra)

        dataretorno = Dataretorno()
        dataretorno.data = request.POST.get('dataR')
        dataretorno.hora = request.POST.get('tempoM')
        dataretorno.atendente = user
        selected_eleitor_id = request.POST.get('cpf')
        selected_eleitor = Eleitor.objects.get(cpf=selected_eleitor_id)

        dataretorno.cliente = selected_eleitor
        dataretorno.save()
        dataretorno.save()

        return redirect('calendario')






@login_required
@has_permission_decorator('calendario')
def calendario_resumo(request):
    if request.method == 'GET':
        search_term = request.GET.get('search')

        # Filtro para pesquisa
        if search_term:
            usuarios = Dataretorno.objects.filter(Q(cliente__nome__icontains=search_term) | Q(cliente__cpf__icontains=search_term) | Q(data__icontains=search_term) | Q(atendente__username__icontains=search_term)).order_by('-data')
        else:
            usuarios = Dataretorno.objects.all().order_by('-data')

        usuario_paginator = Paginator(usuarios, 8)
        page_num = request.GET.get('page')

        try:
            page = usuario_paginator.get_page(page_num)
        except PageNotAnInteger:
            page = usuario_paginator.get_page(1)  # Se o número da página não for um inteiro, vai para a primeira
        except EmptyPage:
            page = usuario_paginator.get_page(usuario_paginator.num_pages)  # Se a página estiver fora do intervalo, pega a última

        # Passa o filtro e a paginação para o template
        context = {
            'page': page,
            'paginator': usuario_paginator,  # Passa o paginator para acessar informações como total de páginas
        }

        # Log do acesso
        user = CustomUser.objects.get(pk=request.user.id)
        extra = {
            'user_id': user.id,
            'username': user.username,
            'ip_address': request.META.get('REMOTE_ADDR')
        }
        logger.info('Acessou a pagina de Calendario Resumo.', extra=extra)

        return render(request, 'calendario_resumo.html', context)




@login_required
@has_permission_decorator('calendario')
def marcar_calendario(request):
        usuarios = {
            'usuarios': Eleitor.objects.all()
        }

        return render(request, 'marcar_calendario.html', usuarios)




def buscar_nome_por_cpf(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        try:
            usuario = Eleitor.objects.get(cpf=cpf)
            return JsonResponse({'nome_completo': usuario.nome})
        except Eleitor.DoesNotExist:
            return JsonResponse({'error': 'CPF não encontrado'})




@login_required
def cadastro(request):
    if request.method == 'GET':
        notificar_atendente()
        user = CustomUser.objects.get(pk=request.user.id)
        extra = {
            'user_id': user.id,
            'username': user.username,
            'ip_address': request.META.get('REMOTE_ADDR')
            }    
        logger.info('Acessou a pagina de CADASTRO.', extra=extra)
        return render(request, "cadastro.html")
    else:
        cpfC = request.POST.get('cpf')
        dataN = request.POST.get('dataN')

        if Eleitor.objects.filter(cpf=cpfC).exists():
                return render(request, 'jaexiste.html')

        if not valida_cpf(cpfC):
            contexto = {
                'cpfI': 'CPF INVÁLIDO, por favor verifique os dados digitados.'
            }
            return render(request, 'cadastro.html', contexto)

        if valida_cpf(cpfC):

            user = CustomUser.objects.get(pk=request.user.id)
            extra = {
                'user_id': user.id,
                'username': user.username,
                'ip_address': request.META.get('REMOTE_ADDR')
                }    
            logger.info('Iniciou o Cadastro, Consultando na Receita...', extra=extra)

            data = datetime.strptime(dataN, '%Y-%m-%d')

            data_formatada = data.strftime("%d/%m/%Y")


            nomeCompleto = extrair_nome_receita(cpfC, data_formatada)


            if nomeCompleto:

                contexto = {
                        'nomeCompleto': nomeCompleto,
                        'cpfC': cpfC,
                        'dataN': dataN,
                    }
                
                user = CustomUser.objects.get(pk=request.user.id)
                extra = {
                'user_id': user.id,
                'username': user.username,
                'ip_address': request.META.get('REMOTE_ADDR')
                }    
                logger.info('Consulta realizada com sucesso.', extra=extra)

                return render(request, 'cadastro2.html', contexto)
            else:
                user = CustomUser.objects.get(pk=request.user.id)
                extra = {
                'user_id': user.id,
                'username': user.username,
                'ip_address': request.META.get('REMOTE_ADDR')
                }    
                logger.error('ERRO AO CONSULTAR NA RECEITA', extra=extra)
                return render(request, 'erro_receita.html')
            



@login_required
@has_permission_decorator('staff')
def apagarEleitor(request, usuario_id):
    if request.method == 'POST':
        Eleitor.objects.filter(id_usuario=usuario_id).delete()
        user = CustomUser.objects.get(pk=request.user.id)
        extra = {
                'user_id': user.id,
                'username': user.username,
                'ip_address': request.META.get('REMOTE_ADDR')
                }    
        logger.warning('Apagou o Eleitor/Eleitor ID: %s',usuario_id,extra=extra)
        return redirect(reverse('eleitores'))
    else:
        return redirect('home')
    


@login_required
@has_permission_decorator('staff')
def confirm_eleitor(request, usuario_id):
    usuario = Eleitor.objects.get(pk=usuario_id)
    if request.method == 'GET':

        contexto = {
                    'usuario': usuario,
                }

        return render(request, "confirm_eleitor.html", contexto)



@login_required
def cadastro2(request):
        if request.method == 'POST':

            atendente = CustomUser.objects.get(username=request.user.username)
            novo_usuario = Eleitor()
            novo_usuario.nome = request.POST.get('nome')
            novo_usuario.nomeS = request.POST.get('nomeS')
            novo_usuario.telefone = request.POST.get('telefone')
            novo_usuario.cpf = request.POST.get('cpf')
            novo_usuario.genero = request.POST.get('exampleRadios')
            novo_usuario.dataN = request.POST.get('dataN')
            novo_usuario.atendente = atendente
            novo_usuario.save()

            usuario_id = novo_usuario.id_usuario
            
            user = CustomUser.objects.get(pk=request.user.id)
            extra = {
            'user_id': user.id,
            'username': user.username,
            'ip_address': request.META.get('REMOTE_ADDR')
            }    
            logger.warning('Cadastro feito por completo. ID:%s', usuario_id,extra=extra)

            if has_role(request.user, 'frente') and not request.user.is_superuser:
                user = request.user
                notificar_role(f"Acabei de cadastrar um novo Eleitor (CPF: {novo_usuario.cpf})", user, "Atendente")
                notificar_role(f"Acabei de cadastrar um novo Eleitor (CPF: {novo_usuario.cpf})", user, "Solucionador")
                notificar_role(f"Acabei de cadastrar um novo Eleitor (CPF: {novo_usuario.cpf})", user, "Staff")
                return render(request, 'usuario_sucesso.html')
            
            request.session['from_cadastro2'] = True

            return redirect('adicionar_endereco', eleitor_id=usuario_id)
        else:
            return redirect('home')



@login_required
def adicionar_endereco(request, eleitor_id):
    eleitor = Eleitor.objects.get(id_usuario=eleitor_id)
    
    if request.method == 'POST':
        # Verifica se já existem endereços para o eleitor
        endereco_principal = Endereco.objects.filter(eleitor=eleitor, principal=True).exists()
        
        # Define se o novo endereço deve ser principal
        if not endereco_principal:
            principal = True
        else:
            # Caso contrário, verifica se o usuário marcou como principal
            principal = 'principal' in request.POST
        
        # Cria o novo endereço
        endereco = Endereco(
            eleitor=eleitor,
            endereco=request.POST.get('endereço'),
            numero=request.POST.get('numero'),
            complemento=request.POST.get('complemento') or '',
            bairro=request.POST.get('bairro'),
            estado=request.POST.get('estado'),
            municipio=request.POST.get('municipio'),
            cep=request.POST.get('txtCep'),
            tipo_endereco=request.POST.get('tipo_endereco'),
            principal=principal
        )
        
        endereco.save()

        if request.session.get('from_cadastro2'):
            del request.session['from_cadastro2']
            return redirect('assunto_inserir', usuario_id=eleitor_id)
        else:
            return redirect('editar_eleitor', usuario_id=eleitor_id)
    
    return render(request, 'adicionar_endereco.html', {'eleitor': eleitor})



@login_required
@has_permission_decorator('usuarios')
def eleitores(request):
    if request.method == 'GET':
        notificar_atendente()
        search_term = request.GET.get('search')
        all_records = request.GET.get('all')

        # Filtro para pesquisa
        if search_term:
            # Filtra Eleitores com base nas informações de Endereco
            usuarios = Eleitor.objects.filter(
                Q(nome__icontains=search_term) | 
                Q(cpf__icontains=search_term) |
                Q(enderecos__bairro__icontains=search_term) |  
                Q(enderecos__municipio__icontains=search_term)  
            ).distinct().order_by('-data_criacao')
        else:
            usuarios = Eleitor.objects.all().order_by('-data_criacao')

        if all_records:
            page = usuarios  # Sem paginação, passa todos os resultados diretamente
            usuario_paginator = None  # Não será utilizado o paginator
        else:
            usuario_paginator = Paginator(usuarios, 8)
            page_num = request.GET.get('page')

            try:
                page = usuario_paginator.get_page(page_num)
            except PageNotAnInteger:
                page = usuario_paginator.get_page(1)
            except EmptyPage:
                page = usuario_paginator.get_page(usuario_paginator.num_pages)

        # Para cada eleitor, obtemos o endereço principal
        eleitores_com_enderecos = []
        for eleitor in page:
            endereco_principal = eleitor.enderecos.filter(principal=True).first()
            eleitores_com_enderecos.append({
                'eleitor': eleitor,
                'endereco_principal': endereco_principal
            })

        # Passa o filtro e a paginação para o template
        context = {
            'page': eleitores_com_enderecos,
            'paginator': usuario_paginator,
        }

        # Log do acesso
        user = CustomUser.objects.get(pk=request.user.id)
        extra = {
            'user_id': user.id,
            'username': user.username,
            'ip_address': request.META.get('REMOTE_ADDR')
        }
        logger.info('Acessou a pagina de Eleitores Cadastrados.', extra=extra)

        return render(request, 'eleitores.html', context)




@login_required
@has_permission_decorator('assunto')
def editar_eleitor(request, usuario_id):
        # Recupere o usuário pela ID
        usuario = Eleitor.objects.get(pk=usuario_id)


        if request.method == 'GET':
            contexto = {
                'usuario': usuario,
            }
            return render(request, 'editar_cadastro.html', contexto)


        elif request.method == 'POST':
            # Atualize os dados do endereço do usuário
            usuario.telefone = request.POST.get('telefone')
            usuario.nomeS = request.POST.get('nomeS')
            usuario.cep = request.POST.get('txtCep')
            usuario.endereço = request.POST.get('endereço')
            usuario.numero = request.POST.get('numero')
            if request.POST.get('complemento') == None:
                usuario.complemento = ' '
            usuario.complemento = request.POST.get('complemento')
            usuario.bairro = request.POST.get('bairro')
            usuario.estado = request.POST.get('estado')
            usuario.municipio = request.POST.get('municipio')

            # Salve as alterações no banco de dados
            usuario.save()

            user = CustomUser.objects.get(pk=request.user.id)
            extra = {
            'usuario.id_usuario': usuario.id_usuario,
            'user_id': user.id,
            'username': user.username,
            'ip_address': request.META.get('REMOTE_ADDR')
            }
            logger.warning('Editou o cadastro do Eleitor. ID: %s', usuario_id,extra=extra)

            # Redirecione para a página do usuário
            return redirect(reverse('eleitores'))


@login_required
@has_permission_decorator('staff')
def editar_endereco(request, endereco_id):
    endereco = get_object_or_404(Endereco, id=endereco_id)

    if request.method == 'POST':
        endereco.cep = request.POST.get('txtCep')
        endereco.endereco = request.POST.get('endereço')
        endereco.numero = request.POST.get('numero')
        endereco.complemento = request.POST.get('complemento')
        endereco.bairro = request.POST.get('bairro')
        endereco.estado = request.POST.get('estado')
        endereco.municipio = request.POST.get('municipio')

        # Verifica se o checkbox 'principal' está marcado
        if 'principal' in request.POST:
            # Se marcado, define como principal
            endereco.principal = True
        else:
            # Se não estiver marcado, verifica se é o único endereço do usuário
            eleitor = endereco.eleitor
            outros_enderecos_principais = Endereco.objects.filter(eleitor=eleitor, principal=True).exclude(id=endereco.id)
            
            if not outros_enderecos_principais.exists():
                # Se não houver outro endereço principal, mantém este como principal
                endereco.principal = True
            else:
                # Se houver outros, pode desmarcar como principal
                endereco.principal = False

        endereco.save()
        return redirect('editar_eleitor', usuario_id=endereco.eleitor.id_usuario)

    return render(request, 'editar_endereco.html', {'endereco': endereco})



@login_required
@has_permission_decorator('staff')
def excluir_endereco(request, endereco_id):
    endereco = get_object_or_404(Endereco, id=endereco_id)

    if request.method == 'POST':
        eleitor_id = endereco.eleitor.id_usuario
        endereco.delete()
        return redirect('editar_eleitor', usuario_id=eleitor_id)



@login_required
@has_permission_decorator('assunto')
def assunto_inserir(request, usuario_id):
        if request.method == 'GET':
            atuacoes = Atuacao.objects.all()
            usuario = Eleitor.objects.get(pk=usuario_id)

            contexto = {
                    'usuario': usuario,
                    'atuacoes': atuacoes
                }
            
            user = CustomUser.objects.get(pk=request.user.id)
            extra = {
                'user_id': user.id,
                'username': user.username,
                'ip_address': request.META.get('REMOTE_ADDR')
                } 
            logger.info('Acessou a pagina de inserir assunto.', extra=extra)
            
            return render(request, 'assunto_inserir.html', contexto)


@login_required
@has_permission_decorator('assunto')
def post_assunto(request):
    if request.method == 'POST':
        atendente = CustomUser.objects.get(username=request.user.username)
        
        assunto_texto = request.POST.get('assuntoT')
        cliente_escolhido_id = request.POST.get('cliente_escolhido_id')
        area_de_atuacao_id = request.POST.get('area_de_atuacao')  # Obtém a área de atuação selecionada

        try:
            cliente_escolhido = Eleitor.objects.get(pk=int(cliente_escolhido_id))
        except (Eleitor.DoesNotExist, ValueError):
            cliente_escolhido = None  # Define como None se não encontrar o cliente

        if cliente_escolhido:
            # Cria o objeto Assunto com a instância do Eleitor e a área de atuação
            novo_assunto = Assunto(
                assuntoT=assunto_texto,
                clienteEscolhido=cliente_escolhido,
                atendente=atendente,
                area_de_atuacao_id=area_de_atuacao_id  # Define a área de atuação
            )
            novo_assunto.save()

            # Notificar os usuários da área de atuação
            # Filtrar os usuários que têm o grupo "Solucionador" e a mesma área de atuação
            solucionadores = CustomUser.objects.filter(
                atuacoes=area_de_atuacao_id
            )

            for solucionador in solucionadores:
                if has_role(solucionador, 'solucionador'):
                    notify.send(
                        request.user, 
                        recipient=solucionador,
                        verb=f'Inseri um novo assunto na sua área de atuação! CPF: ({cliente_escolhido.cpf})'
                    )

            user = CustomUser.objects.get(pk=request.user.id)
            extra = {
                'user_id': user.id,
                'username': user.username,
                'ip_address': request.META.get('REMOTE_ADDR')
            }
            logger.warning('Inseriu um Assunto no Eleitor: ID: %s', cliente_escolhido_id, extra=extra)
        else:
            user = CustomUser.objects.get(pk=request.user.id)
            extra = {
                'user_id': user.id,
                'username': user.username,
                'ip_address': request.META.get('REMOTE_ADDR')
            }
            logger.error('Erro ao inserir um Assunto no Eleitor. ID: %s', cliente_escolhido_id, extra=extra)
        
        request.session['assunto_criado'] = True
        return redirect('assunto_sucesso')
    else:
        return redirect('home')


@login_required
@has_permission_decorator('assunto')
def assunto_sucesso(request):
    if not request.session.get('assunto_criado'):
        return redirect('home')


    del request.session['assunto_criado']

    return render(request, 'assunto_sucesso.html')




@login_required
@has_permission_decorator('assunto_lista')
def assuntos(request):
    if request.method == 'GET':
        notificar_atendente()
        search_term = request.GET.get('search')
        all_records = request.GET.get('all')

        # Obtém o usuário atual
        user = CustomUser.objects.get(pk=request.user.id)
        atuacoes = user.atuacoes.all()

        # Filtro para pesquisa
        if search_term:
            if user.has_perm('appCampanha.staff'):
                usuarios = Assunto.objects.filter(
                    Q(clienteEscolhido__nome__icontains=search_term) | 
                    Q(clienteEscolhido__cpf__icontains=search_term) | 
                    Q(assuntoT__icontains=search_term)
                ).order_by('-data_criacao')
            else:
                filtro_area_atuacao = Assunto.objects.filter(area_de_atuacao__usuarios=user)
                if search_term:
                    usuarios = filtro_area_atuacao.filter(
                        Q(clienteEscolhido__nome__icontains=search_term) | 
                        Q(clienteEscolhido__cpf__icontains=search_term) | 
                        Q(assuntoT__icontains=search_term)
                    ).order_by('-data_criacao')
        else:
            # Filtra por área de atuação se não for superuser
            if user.has_perm('appCampanha.staff'):
                usuarios = Assunto.objects.all().order_by('-data_criacao')
            else:
                usuarios = Assunto.objects.filter(
                area_de_atuacao__usuarios=user  # Filtro correto para área de atuação
            ).order_by('-data_criacao')

        if all_records:
            page = usuarios  # Sem paginação, passa todos os resultados diretamente
            usuario_paginator = None  # Não será utilizado o paginator
        else:
            usuario_paginator = Paginator(usuarios, 8)
            page_num = request.GET.get('page')

            try:
                page = usuario_paginator.get_page(page_num)
            except PageNotAnInteger:
                page = usuario_paginator.get_page(1)  # Se o número da página não for um inteiro, vai para a primeira
            except EmptyPage:
                page = usuario_paginator.get_page(usuario_paginator.num_pages)  # Se a página estiver fora do intervalo, pega a última

        # Passa o filtro e a paginação para o template
        context = {
            'page': page,
            'paginator': usuario_paginator,
            'atuacoes': atuacoes,
            'user': user
        }

        # Log do acesso
        extra = {
            'user_id': user.id,
            'username': user.username,
            'ip_address': request.META.get('REMOTE_ADDR')
        }
        logger.info('Acessou a pagina de Assuntos.', extra=extra)

        return render(request, 'assuntos.html', context)




@login_required
@has_permission_decorator('staff')
def apagarAssunto(request, assunto_id):
    if request.method == 'POST':
        Assunto.objects.filter(id_assunto=assunto_id).delete()
        user = CustomUser.objects.get(pk=request.user.id)
        extra = {
                'user_id': user.id,
                'username': user.username,
                'ip_address': request.META.get('REMOTE_ADDR')
                }    
        logger.warning('Apagou o Assunto ID: %s',assunto_id,extra=extra)
        return redirect(reverse('assuntos'))
    else:
        return redirect('home')



@login_required
@has_permission_decorator('staff') 
def confirm_assunto(request, assunto_id):
    assunto = Assunto.objects.get(pk=assunto_id)

    if request.method == 'GET':

        contexto = {
                    'assunto': assunto,
                }

        return render(request, "confirm_assunto.html", contexto)




@login_required
@has_permission_decorator('assunto')
def gerenciar_atendimento(request, assunto_id):
    assunto = get_object_or_404(Assunto, id_assunto=assunto_id)
    
    if request.method == 'POST':
        if 'descricao' in request.POST:
            # Adicionar nova observação
            descricao = request.POST.get('descricao')
            observacao = Observacao(assunto=assunto, descricao=descricao, atendente=request.user)
            observacao.save()

            user = CustomUser.objects.get(pk=request.user.id)
            extra = {
                'user_id': user.id,
                'username': user.username,
                'ip_address': request.META.get('REMOTE_ADDR')
                }    
            logger.warning('Adicionou uma observação no Assunto ID: %s',assunto_id,extra=extra)
        
        # Se o atendimento foi iniciado, mudar o status
        if assunto.status == 'Pendente':
            assunto.status = 'Em Atendimento'
            assunto.save()

            user = CustomUser.objects.get(pk=request.user.id)
            extra = {
                'user_id': user.id,
                'username': user.username,
                'ip_address': request.META.get('REMOTE_ADDR')
                }    
            logger.warning('Iniciou o atendimento do Assunto ID: %s',assunto_id,extra=extra)

        return redirect('gerenciar_atendimento', assunto_id=assunto.id_assunto)


    if not request.user.is_superuser:
         if assunto.area_de_atuacao and not request.user.atuacoes.filter(id=assunto.area_de_atuacao.id).exists():
            return render(request, '403.html')

    # Pegar as observações para exibir
    observacoes = assunto.observacoes.all()

    if assunto.status == 'Finalizado':
        return redirect('assunto_detalhes', assunto_id=assunto_id)
    
    return render(request, 'gerenciar_atendimento.html', {'assunto': assunto, 'observacoes': observacoes})




@login_required
@has_permission_decorator('solucao')
def finalizar_atendimento(request, assunto_id):
    # Busca o Assunto específico
    assunto = get_object_or_404(Assunto, pk=assunto_id)
    
    # Finalizar atendimento
    if request.method == 'POST':
        solucionado = request.POST.get('solucionado')
        assunto.motivo_finalizacao = request.POST.get('motivo_finalizacao')
        assunto.status = 'Finalizado'
        assunto.solucionado = solucionado
        assunto.finalizado_por = request.user
        assunto.data_finalizacao = timezone.now()
        assunto.save()

        notify.send(
            request.user,
            recipient=assunto.atendente,
            verb=f'Finalizei o assunto que você criou, acesse o relatório para verificar! CPF: {assunto.clienteEscolhido.cpf}',
            target=assunto,
        )

        user = CustomUser.objects.get(pk=request.user.id)
        extra = {
            'user_id': user.id,
            'username': user.username,
            'ip_address': request.META.get('REMOTE_ADDR')
            }    
        logger.warning('Finalizou o Assunto ID: %s',assunto_id,extra=extra)

    return redirect('assunto_detalhes', assunto_id=assunto_id)




@login_required
@has_permission_decorator('assunto')
def assunto_detalhes(request, assunto_id):
    assunto = get_object_or_404(Assunto, id_assunto=assunto_id)
    observacoes = assunto.observacoes.all()

    return render(request, 'assunto_detalhes.html', {'assunto': assunto, 'observacoes': observacoes})




@login_required
@has_permission_decorator('staff')
def tabela_usuario(request):

    if request.method == 'GET':
        search_term = request.GET.get('search')

        # Filtro para pesquisa
        if search_term:
            usuarios = CustomUser.objects.filter(Q(username__icontains=search_term))
        else:
            usuarios = CustomUser.objects.all()

        usuario_paginator = Paginator(usuarios, 8)
        page_num = request.GET.get('page')

        try:
            page = usuario_paginator.get_page(page_num)
        except PageNotAnInteger:
            page = usuario_paginator.get_page(1)  # Se o número da página não for um inteiro, vai para a primeira
        except EmptyPage:
            page = usuario_paginator.get_page(usuario_paginator.num_pages)  # Se a página estiver fora do intervalo, pega a última

        # Passa o filtro e a paginação para o template
        context = {
            'page': page,
            'paginator': usuario_paginator,  # Passa o paginator para acessar informações como total de páginas
        }

        # Log do acesso
        user = CustomUser.objects.get(pk=request.user.id)
        extra = {
            'user_id': user.id,
            'username': user.username,
            'ip_address': request.META.get('REMOTE_ADDR')
        }
        logger.warning('Acessou a pagina de RELATÓRIOS USERS.', extra=extra)

        return render(request, 'tabela_usuario.html', context)



@login_required
@has_permission_decorator('usuarios')
def tabela_eleitor(request):

    if request.method == 'GET':
        search_term = request.GET.get('search')
        all_records = request.GET.get('all')

        # Filtro para pesquisa
        if search_term:
            usuarios = Eleitor.objects.filter(Q(nome__icontains=search_term) | Q(cpf__icontains=search_term) | Q(data_criacao__icontains=search_term) | Q(atendente__username__icontains=search_term)).order_by('-data_criacao')
        else:
            usuarios = Eleitor.objects.all().order_by('-data_criacao')

        
        if all_records:
            page = usuarios
            usuario_paginator = None
        
        else:
            usuario_paginator = Paginator(usuarios, 8)
            page_num = request.GET.get('page')

            try:
                page = usuario_paginator.get_page(page_num)
            except PageNotAnInteger:
                page = usuario_paginator.get_page(1)
            except EmptyPage:
                page = usuario_paginator.get_page(usuario_paginator.num_pages)


        context = {
            'page': page,
            'paginator': usuario_paginator,
        }

        # Log do acesso
        user = CustomUser.objects.get(pk=request.user.id)
        extra = {
            'user_id': user.id,
            'username': user.username,
            'ip_address': request.META.get('REMOTE_ADDR')
        }
        logger.warning('Acessou a pagina de RESUMO ELEITOR.', extra=extra)

        return render(request, 'tabela_eleitor.html', context)





@login_required
@has_permission_decorator('usuarios')
def relatorio_eleitor(request, usuario_id):
    usuarios = Eleitor.objects.get(pk=usuario_id)

    assuntos = Assunto.objects.filter(clienteEscolhido=usuarios)
    dataretornos = Dataretorno.objects.filter(cliente=usuarios)

    contexto = {
        'usuarios': usuarios,
        'assuntos': assuntos,
        'dataretornos': dataretornos
    }

    user = CustomUser.objects.get(pk=request.user.id)
    extra = {
        'user_id': user.id,
        'username': user.username,
        'ip_address': request.META.get('REMOTE_ADDR')
    }
    logger.warning('Acessou o relatório do Eleitor ID: %s', usuarios.id_usuario, extra=extra)

    return render(request, 'relatorio_eleitor.html', contexto)

        


@login_required
@has_permission_decorator('staff')
def relatorio_usuario(request, user_id):
    usuario_atual = get_object_or_404(CustomUser, id=user_id)

    # Captura a busca
    search_query = request.GET.get('search', '')

    # Inicializa listas vazias
    eleitores = []
    assuntos = []
    dataretornos = []
    observacoes_por_assunto = {}

    # Busca de eleitores
    if search_query:
        eleitores = Eleitor.objects.filter(nome__icontains=search_query) | Eleitor.objects.filter(cpf__icontains=search_query)
    else:
        eleitores = Eleitor.objects.all()

    paginator = Paginator(eleitores, 1)
    page_number = request.GET.get('page')
    usuarios_page_obj = paginator.get_page(page_number)

    # Verifica se há um eleitor na página atual
    eleitor_atual = usuarios_page_obj[0] if usuarios_page_obj else None

    # Filtra dados relacionados ao atendente e ao eleitor atual
    if eleitor_atual:
        assuntos = Assunto.objects.filter(atendente=usuario_atual, clienteEscolhido=eleitor_atual)
        for assunto in assuntos:
            observacoes_por_assunto[assunto.id_assunto] = Observacao.objects.filter(atendente=usuario_atual, assunto=assunto)
        dataretornos = Dataretorno.objects.filter(atendente=usuario_atual, cliente=eleitor_atual)

    context = {
        'user': usuario_atual,
        'usuarios_page_obj': usuarios_page_obj,
        'assuntos': assuntos,
        'observacoes_por_assunto': observacoes_por_assunto,
        'dataretornos': dataretornos,
        'search_query': search_query,
    }
    
    return render(request, 'relatorio_usuario.html', context)





@login_required
@has_permission_decorator('staff')
def dashboard(request):

    # Contar registros das tabelas Eleitor, Assunto e Dataretorno
    total_eleitores = Eleitor.objects.all().count()
    total_assunto = Assunto.objects.all().count()
    eleitores = Eleitor.objects.order_by('-data_criacao')[:7]

    agendamentos_ultimos_7 = Dataretorno.objects.order_by('-data')[:7]
    total_dataretornos = Dataretorno.objects.all().count()

    today = timezone.now().date()
    seven_days_ago = today - timedelta(days=6)

    cadastros_por_dia = {}
    assuntos_por_dia = {}
    solucoes_por_dia = {}

    for i in range(7):
        day = seven_days_ago + timedelta(days=i)
        
        # Converte 'day' para datetime ciente do fuso horário
        day_start = timezone.make_aware(timezone.datetime.combine(day, timezone.datetime.min.time()))
        day_end = timezone.make_aware(timezone.datetime.combine(day, timezone.datetime.max.time()))
        
        # Filtra os cadastros e assuntos entre o início e o fim do dia
        cadastros = Eleitor.objects.filter(data_criacao__range=[day_start, day_end]).count()

        # Total de assuntos finalizados ou parcialmente solucionados no dia
        total_solucoes = Assunto.objects.filter(
            data_finalizacao__range=[day_start, day_end], 
            solucionado__in=['Solucionado', 'Parcialmente Solucionado']
        ).count()

        # Total de novos assuntos criados no dia
        total_assuntos = Assunto.objects.filter(data_criacao__range=[day_start, day_end]).count()

        solucoes_por_dia[day.strftime('%d/%m/%Y')] = total_solucoes
        cadastros_por_dia[day.strftime('%d/%m/%Y')] = cadastros
        assuntos_por_dia[day.strftime('%d/%m/%Y')] = total_assuntos

    assuntos2 = Assunto.objects.order_by('-data_criacao')[:7]

    # Contagem por gênero
    genero_distribuicao = Eleitor.objects.values('genero').annotate(total=Count('genero'))

    # Contagem por bairro
    bairro_distribuicao = Endereco.objects.values('bairro').annotate(total=Count('bairro')).order_by('-total')

    # Dados para o gráfico de gênero
    generos = [entry['genero'] for entry in genero_distribuicao]
    genero_totais = [entry['total'] for entry in genero_distribuicao]

    # Dados para o gráfico de bairros
    bairros = [entry['bairro'] for entry in bairro_distribuicao]
    bairro_totais = [entry['total'] for entry in bairro_distribuicao]

    total_generos = sum(genero_totais)
    total_bairros = sum(bairro_totais)

    hoje = now().date()
    eleitores_hoje = Eleitor.objects.filter(data_criacao__date=hoje).count()

    inicio_mes = hoje.replace(day=1)
    eleitores_mes = Eleitor.objects.filter(data_criacao__date__gte=inicio_mes).count()

    total_assuntos2 = Assunto.objects.count()

    # Assuntos que foram finalizados (independente da solução)
    assuntos_com_solucao = Assunto.objects.filter(status='finalizado').count()

    # Calcula a porcentagem de resolução
    if total_assuntos2 > 0:
        porcentagem_resolucao = (assuntos_com_solucao / total_assuntos2) * 100
    else:
        porcentagem_resolucao = 0

    desempenho = (
        CustomUser.objects.annotate(
            cadastros=Count('eleitor', distinct=True),
            assuntos=Count('assunto', distinct=True),
            solucoes=Count('assunto', filter=Q(assunto__solucionado__in=['Solucionado', 'Parcialmente Solucionado']), distinct=True)
        )
        .values('username', 'cadastros', 'assuntos', 'solucoes', 'id')
        .order_by('-cadastros')
    )

    context = {
        'labels': list(cadastros_por_dia.keys()),
        'data': list(cadastros_por_dia.values()),
        'solucoes': list(solucoes_por_dia.values()),
        'assuntos': list(assuntos_por_dia.values()),
        'total_eleitores': total_eleitores,
        'total_assuntos': total_assunto,
        'total_solucoes': sum(solucoes_por_dia.values()),
        'total_dataretornos': total_dataretornos,
        'agendamentos_hoje': agendamentos_ultimos_7,
        'eleitores': eleitores,
        'assuntos2': assuntos2,
        'generos': generos,
        'genero_totais': genero_totais,
        'bairros': bairros,
        'bairro_totais': bairro_totais,
        'total_generos': total_generos,
        'total_bairros': total_bairros,
        'eleitores_hoje': eleitores_hoje,
        'eleitores_mes': eleitores_mes,
        'porcentagem_resolucao': porcentagem_resolucao,
        'desempenho_atendentes': desempenho,
    }

    user = CustomUser.objects.get(pk=request.user.id)
    extra = {
            'user_id': user.id,
            'username': user.username,
            'ip_address': request.META.get('REMOTE_ADDR')
                }    
    logger.warning('Acessou o DASHBOARD.', extra=extra)

    return render(request, 'dashboard.html', context)





def calculate_data_for_period(start_date, end_date):
    # Calcula os dias entre o start_date e o end_date (incluindo o end_date no intervalo)
    num_days = (end_date - start_date).days + 1

    # Lista de rótulos para os dias
    labels = [(start_date + timedelta(days=i)).strftime('%d/%m/%Y') for i in range(num_days)]

    # Dados para cadastros, assuntos e soluções
    data_cadastros = []
    data_assuntos = []
    data_solucoes = []

    for i in range(num_days):
        day = start_date + timedelta(days=i)
        
        # Definindo o início e o fim do dia
        day_start = timezone.make_aware(timezone.datetime.combine(day, timezone.datetime.min.time()))
        day_end = timezone.make_aware(timezone.datetime.combine(day, timezone.datetime.max.time()))
        
        # Contando os cadastros, assuntos e soluções do dia
        cadastros = Eleitor.objects.filter(data_criacao__range=[day_start, day_end]).count()
        assuntos = Assunto.objects.filter(data_criacao__range=[day_start, day_end]).count()
        solucoes = Assunto.objects.filter(
            data_finalizacao__range=[day_start, day_end], 
            solucionado__in=['Solucionado', 'Parcialmente Solucionado']
        ).count()
        
        # Adiciona os resultados nas listas correspondentes
        data_cadastros.append(cadastros)
        data_assuntos.append(assuntos)
        data_solucoes.append(solucoes)
    
    # Retorna os dados em uma tupla, incluindo labels
    return labels, data_cadastros, data_assuntos, data_solucoes





@login_required
def get_data(request, period):
    today = timezone.now().date()
    start_date = today - timedelta(days=int(period))

    # Função que calcula os dados para o período
    labels, data, assuntos, solucoes = calculate_data_for_period(start_date, today)




    return JsonResponse({
        'labels': labels,
        'cadastros': data,
        'assuntos': assuntos,
        'solucoes': solucoes,
    })




@login_required
def edit_profile(request):
    user = request.user
    atuacoes = user.atuacoes.all()
    
    if request.method == 'POST':
        # Atualizando os campos básicos de perfil
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)

        # Verificando se a remoção da imagem de perfil foi solicitada
        remove_profile_image = request.POST.get('remove_profile_image', 'false') == 'true'

        if remove_profile_image:
            if user.profile_image:
                user.profile_image.delete(save=False)
            user.profile_image = None

        # Verificando se uma nova imagem foi enviada
        elif 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
        
        user.save()

        messages.success(request, 'Seu perfil foi atualizado com sucesso.')
        return redirect('edit_profile')
    
    return render(request, 'edit_profile.html', {'user': user, 'atuacoes': atuacoes})