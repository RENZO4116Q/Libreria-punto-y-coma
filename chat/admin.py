from django.contrib import admin
from .models import ConsultaIA


@admin.register(ConsultaIA)
class ConsultaIAAdmin(admin.ModelAdmin):

    list_display = (
        "fecha",
        "pregunta_corta",
        "modelo",
        "exitosa",
    )

    list_filter = (
        "exitosa",
        "modelo",
        "fecha",
    )

    search_fields = (
        "pregunta",
        "respuesta",
    )

    readonly_fields = (
        "fecha",
    )

    def pregunta_corta(self, obj):
        return obj.pregunta[:60]

    pregunta_corta.short_description = "Pregunta"