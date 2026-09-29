from django.db import models


class ConsultaIA(models.Model):

    TIPOS_RESULTADO = [
    ("ia", "Procesada por IA"),
    ("rechazada", "Rechazada por ámbito"),
    ("error", "Error de Ollama"),
    ]

    pregunta = models.TextField(
        verbose_name="Pregunta"
    )

    respuesta = models.TextField(
        verbose_name="Respuesta"
    )

    fecha = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de consulta"
    )

    modelo = models.CharField(
        max_length=100,
        default="productos-qwen2.5",
        verbose_name="Modelo utilizado"
    )

    exitosa = models.BooleanField(
        default=True,
        verbose_name="Consulta exitosa"
    )

    tipo_resultado = models.CharField(
        max_length=20,
        choices=TIPOS_RESULTADO,
        default="ia",
    )
    class Meta:
        verbose_name = "Consulta de IA"
        verbose_name_plural = "Consultas de IA"
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.fecha:%d/%m/%Y %H:%M} - {self.pregunta[:50]}"