from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser

from projetoCampanha import settings

class Atuacao(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

# Extensão do modelo de Usuário
class CustomUser(AbstractUser):
    atuacoes = models.ManyToManyField(Atuacao, related_name='usuarios')
    profile_image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_first_login = models.BooleanField(default=True)

    def __str__(self):
        return self.username

class Senha(models.Model):
    numero = models.IntegerField(unique=True)
    data_criacao = models.DateTimeField(default=now)
    atendida = models.BooleanField(default=False)
    chamada = models.DateTimeField(null=True, blank=True)
    atendente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['numero']

    def __str__(self):
        return f'Senha {self.numero}'
    
    @property
    def tempo_espera(self):
        if self.chamada and self.data_criacao:
            espera = self.chamada - self.data_criacao
            total_seconds = int(espera.total_seconds())
            horas, resto = divmod(total_seconds, 3600)
            minutos, segundos = divmod(resto, 60)
            return f"{horas:02}:{minutos:02}:{segundos:02}"  # Formato HH:MM:SS
        return "00:00:00"

class Eleitor(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nome = models.TextField(max_length='255')
    nomeS = models.TextField(max_length='255', null= True)
    telefone = models.TextField(max_length='16', null= True)
    cpf = models.TextField(max_length='14')
    dataN = models.DateField()
    genero = models.TextField(max_length='255', null= True)
    data_criacao = models.DateTimeField(default=now)
    atendente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.nome
    
    def telefone_formatado(self):
        # Remove caracteres não numéricos
        telefone_numeros = ''.join(filter(str.isdigit, self.telefone))
        # Formata o telefone no padrão internacional
        return f"55{telefone_numeros}"

    def link_whatsapp(self):
        telefone_formatado = self.telefone_formatado()
        return f"https://wa.me/{telefone_formatado}"



class Endereco(models.Model):
    eleitor = models.ForeignKey(Eleitor, on_delete=models.CASCADE, related_name='enderecos')
    cep = models.TextField(max_length='9')
    endereco = models.TextField(max_length='255')
    numero = models.IntegerField(null=True)
    complemento = models.TextField(max_length='255', null=True)
    bairro = models.TextField(max_length='255')
    estado = models.TextField(max_length='255')
    municipio = models.TextField(max_length='255')
    tipo_endereco = models.CharField(max_length=20, choices=[
        ('Caixa Postal', 'Caixa Postal'),
        ('Residencial', 'Residencial'),
        ('Comercial', 'Comercial'),
    ])
    principal = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.principal:
            Endereco.objects.filter(eleitor=self.eleitor, principal=True).update(principal=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.endereco}, {self.numero} - {self.municipio}/{self.estado}"





class Assunto(models.Model):
    id_assunto = models.AutoField(primary_key=True)
    assuntoT = models.TextField(max_length='255')
    clienteEscolhido = models.ForeignKey(Eleitor, on_delete=models.CASCADE, related_name='cliente_escolhido_id')
    data_criacao = models.DateTimeField(default=now)
    atendente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    area_de_atuacao = models.ForeignKey(Atuacao, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('Pendente', 'Pendente'),
        ('Em Atendimento', 'Em Atendimento'),
        ('Finalizado', 'Finalizado')
    ], default='Pendente')

    solucionado = models.CharField(max_length=24, choices=[
        ('Não Solucionado', 'Não Solucionado'),
        ('Parcialmente Solucionado', 'Parcialmente Solucionado'),
        ('Solucionado', 'Solucionado')
    ], null=True, blank=True)
    motivo_finalizacao = models.TextField(null=True, blank=True)
    finalizado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='finalizador')
    data_finalizacao = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.clienteEscolhido.nome
    

class Observacao(models.Model):
    assunto = models.ForeignKey(Assunto, on_delete=models.CASCADE, related_name='observacoes')
    descricao = models.TextField(max_length=500)
    data_criacao = models.DateTimeField(default=now)
    atendente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Observação do Assunto {self.assunto.id_assunto} em {self.assunto.clienteEscolhido.cpf}"
    


class Dataretorno(models.Model):
    id_dataretorno = models.AutoField(primary_key=True)
    data = models.DateField()
    hora = models.TimeField()
    cliente = models.ForeignKey(Eleitor, on_delete=models.CASCADE)
    atendente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    notificacao_enviada_dia = models.BooleanField(default=False)
    notificacao_enviada_30min = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.cliente.nome
    