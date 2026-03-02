from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from .models import Feriado, Solicitacao

# Register your models here.
class SolicitacaoAdmin(admin.ModelAdmin):
    readonly_fields = ['data_criacao']
    actions = ['aprovar_solicitacoes']

    def aprovar_solicitacoes(self, request, queryset):
        for solicitacao in queryset:
            Feriado.objects.create(
                name = solicitacao.name,
                day = solicitacao.day,
                month = solicitacao.month,
                estado = solicitacao.estado,
                municipio = solicitacao.municipio,
                escopo =  solicitacao.escopo
            )
        status = queryset.update(status="Aprovada")
        self.message_user(
            request,
            ngettext(
                "%d feriado foi aprovado.",
                "%d feriados foram aprovados.",
                status,
            )
            % status,
            messages.SUCCESS,
        )
    aprovar_solicitacoes.short_description = "Aprovar as seguintes solicitacoes"
    

admin.site.register(Feriado)
admin.site.register(Solicitacao, SolicitacaoAdmin)
