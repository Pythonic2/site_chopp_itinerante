from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Evento

class CustomUserAdmin(UserAdmin):
    # Campos a serem exibidos no formulário de criação de usuário
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email'),
        }),
    )

    # Campos a serem exibidos na lista de usuários
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Evento)