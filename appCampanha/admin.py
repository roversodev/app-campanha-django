from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth import get_user_model
from .models import Eleitor, Assunto, Dataretorno, Senha, Atuacao, CustomUser


admin.site.site_header = "Brasil Admin"
admin.site.site_title = "Admin"
admin.site.index_title = "Brasil"

# Tente desregistrar o usuário padrão se ele estiver registrado
User = get_user_model()
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


# Crie um formulário personalizado para o CustomUser
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
    
    # O campo atuacoes vai mostrar um MultipleChoiceField baseado nos registros de Atuacao
    atuacoes = forms.ModelMultipleChoiceField(
        queryset=Atuacao.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


# Personalização do CustomUserAdmin
class CustomUserAdmin(UserAdmin):
    form = CustomUserForm
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'id')

    search_fields = ('username', 'email', 'first_name', 'last_name', 'id')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email', 'is_first_login','profile_image')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
        ('Outras Informações', {'fields': ('atuacoes',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'atuacoes', 'profile_image'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)




@admin.register(Assunto)
class AssuntoAdmin(admin.ModelAdmin):
    list_display = ('clienteEscolhido', 'data_criacao', 'atendente', 'area_de_atuacao','id_assunto')
    search_fields = ('clienteEscolhido__nome', 'clienteEscolhido__cpf')
    list_filter = ('atendente', 'data_criacao')


@admin.register(Eleitor)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'dataN', 'atendente', 'id_usuario')
    search_fields = ('nome', 'cpf')
    list_filter = ('atendente', 'data_criacao')


@admin.register(Dataretorno)
class DataretornoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'data', 'hora', 'id_dataretorno')
    search_fields = ('cliente__nome', 'cliente__cpf')
    list_filter = ('atendente',)


@admin.register(Atuacao)
class AtuacaoAdmin(admin.ModelAdmin):
    search_fields = ('nome',)
    list_display = ('id', 'nome')


@admin.register(Senha)
class AssuntoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'data_criacao', 'atendida')