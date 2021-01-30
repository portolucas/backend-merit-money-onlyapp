from django.contrib import admin
from .models import Cargo, Setor, Premios, Transacao, TransacaoPremios, Colaborador
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Cargo)
admin.site.register(Setor)
admin.site.register(Premios)
admin.site.register(Transacao)
admin.site.register(TransacaoPremios)
admin.site.register(Colaborador)


# Define an inline admin descriptor for Colaborador model
# which acts a bit like a singleton
class ColaboradorInline(admin.StackedInline):
    model = Colaborador
    can_delete = False
    verbose_name_plural = 'Colaborador'

# Define a new User admin


class UserAdmin(BaseUserAdmin):
    inlines = (ColaboradorInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
