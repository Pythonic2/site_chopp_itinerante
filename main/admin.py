from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Produto, Transacao, Carrinho,ItemCarrinho

class CustomUserAdmin(UserAdmin):
    # Campos a serem exibidos no formulário de criação de usuário
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'nome', 'email', 'celular', 'bairro', 'endereco', 'data_evento', 'tipo_evento'),
        }),
    )

    # Campos a serem exibidos na lista de usuários
    list_display = ('username', 'nome', 'email', 'celular', 'bairro', 'endereco', 'data_evento', 'tipo_evento', 'is_staff', 'is_superuser')
    search_fields = ('username', 'nome', 'email', 'celular', 'bairro', 'endereco', 'data_evento', 'tipo_evento')
    ordering = ('username',)

    # Campos a serem exibidos no formulário de edição
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('nome', 'email', 'celular', 'bairro', 'endereco', 'data_evento', 'tipo_evento')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(Produto)
admin.site.register(Transacao)
admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Carrinho)
admin.site.register(ItemCarrinho)
