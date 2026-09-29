from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from productos.models import Producto

from .models import ConsultaIA
from .ollama_api import generate_response, MODELO_OLLAMA


# =====================================================
# PALABRAS RELACIONADAS CON EL INVENTARIO
# =====================================================

PALABRAS_INVENTARIO = [
    # Productos
    "producto",
    "productos",
    "articulo",
    "articulos",
    "inventario",

    # Librería
    "libro",
    "libros",
    "libreria",
    "literatura",
    "cuento",
    "cuentos",
    "novela",
    "novelas",

    # Papelería / oficina
    "papeleria",
    "cuaderno",
    "cuadernos",
    "lapiz",
    "lapices",
    "boligrafo",
    "boligrafos",
    "marcador",
    "marcadores",
    "papel",
    "archivador",
    "archivadores",
    "carpeta",
    "carpetas",

    # Atributos
    "codigo",
    "nombre",
    "descripcion",
    "categoria",
    "categorias",
    "precio",
    "precios",
    "cantidad",
    "cantidades",
    "existencia",
    "existencias",
    "stock",
    "estado",
    "fecha",

    # Consultas frecuentes
    "caro",
    "cara",
    "caros",
    "caras",
    "barato",
    "barata",
    "baratos",
    "baratas",
    "agotado",
    "agotados",
    "disponible",
    "disponibles",
]


def pregunta_permitida(pregunta):
    """
    Validación básica para impedir que preguntas claramente
    ajenas al inventario lleguen al modelo de Ollama.
    """

    texto = pregunta.lower()

    return any(
        palabra in texto
        for palabra in PALABRAS_INVENTARIO
    )


# =====================================================
# CHAT
# =====================================================

@require_http_methods(["GET", "POST"])
def chat_view(request):

    respuesta = None
    pregunta = ""
    error = None

    if request.method == "POST":

        pregunta = request.POST.get(
            "user_input",
            ""
        ).strip()

        # ---------------------------------------------
        # Pregunta vacía
        # ---------------------------------------------

        if not pregunta:

            error = "Escribe una pregunta antes de enviar."

        # ---------------------------------------------
        # Pregunta fuera del ámbito
        # ---------------------------------------------

        elif not pregunta_permitida(pregunta):

            respuesta = (
                "Solo puedo responder consultas sobre "
                "productos y sus atributos."
            )

            ConsultaIA.objects.create(
                pregunta=pregunta,
                respuesta=respuesta,
                modelo="Validación Django",
                exitosa=True,
                tipo_resultado="rechazada",
            )

        # ---------------------------------------------
        # Pregunta válida
        # ---------------------------------------------

        else:

            productos = Producto.objects.filter(
                estado=True
            ).order_by("codigo")

            if not productos.exists():

                respuesta = (
                    "No encontré información suficiente en el "
                    "inventario para responder esa pregunta."
                )

                ConsultaIA.objects.create(
                    pregunta=pregunta,
                    respuesta=respuesta,
                    modelo="Validación Django",
                    exitosa=True,
                    tipo_resultado="rechazada",
                )

            else:

                try:

                    respuesta = generate_response(
                        pregunta,
                        productos,
                    )

                    ConsultaIA.objects.create(
                        pregunta=pregunta,
                        respuesta=respuesta,
                        modelo=MODELO_OLLAMA,
                        exitosa=True,
                        tipo_resultado="ia",
                    )

                except Exception:

                    error = (
                        "No fue posible comunicarse con Ollama. "
                        "Comprueba que el servicio esté disponible."
                    )

                    ConsultaIA.objects.create(
                        pregunta=pregunta,
                        respuesta=error,
                        modelo=MODELO_OLLAMA,
                        exitosa=False,
                        tipo_resultado="error",
                    )

    contexto = {
        "pregunta": pregunta,
        "respuesta": respuesta,
        "error": error,
    }

    return render(
        request,
        "chat.html",
        contexto,
    )

def historial_view(request):

    consultas = ConsultaIA.objects.all()

    contexto = {
        "consultas": consultas,

        "total_consultas": consultas.count(),

        "consultas_ia": consultas.filter(
            tipo_resultado="ia"
        ).count(),

        "consultas_rechazadas": consultas.filter(
            tipo_resultado="rechazada"
        ).count(),

        "consultas_error": consultas.filter(
            tipo_resultado="error"
        ).count(),
    }

    return render(
        request,
        "historial.html",
        contexto,
    )