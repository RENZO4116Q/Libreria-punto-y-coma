import json
import ollama

from django.conf import settings


MODELO_OLLAMA = settings.OLLAMA_MODEL

cliente_ollama = ollama.Client(
    host=settings.OLLAMA_HOST
)

def preparar_inventario(productos):
    """
    Convierte los productos de Django a una estructura simple
    que pueda enviarse a Ollama.
    """

    inventario = []

    for producto in productos:

        inventario.append({
            "codigo": producto.codigo,
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "categoria": producto.get_categoria_display(),
            "precio": str(producto.precio),
            "cantidad_existente": producto.cantidad_existente,
            "stock_minimo": producto.stock_minimo,
            "estado": "Activo" if producto.estado else "Inactivo",
            "fecha_registro": producto.fecha_registro.strftime(
                "%d/%m/%Y"
            ),
        })

    return inventario


def generate_response(pregunta, productos):
    """
    Envía a Ollama la pregunta junto con los productos
    registrados actualmente en SQLite.
    """

    inventario = preparar_inventario(productos)

    inventario_json = json.dumps(
        inventario,
        ensure_ascii=False,
        indent=2,
    )

    prompt = f"""
INVENTARIO:
{inventario_json}

PREGUNTA DEL USUARIO:
{pregunta}

INSTRUCCIONES:
Responde exclusivamente utilizando los datos incluidos en INVENTARIO.

No inventes información.

Si INVENTARIO no contiene datos suficientes para responder una pregunta
relacionada con productos, responde exactamente:

No encontré información suficiente en el inventario para responder esa pregunta.

Si la pregunta no está relacionada con productos o inventario, responde
exactamente:

Solo puedo responder consultas sobre productos y sus atributos.
"""

    try:

        respuesta = cliente_ollama.chat(
            model=MODELO_OLLAMA,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            stream=False,
        )

        return respuesta["message"]["content"].strip()

    except Exception as error:

        print(
            f"Error al comunicarse con Ollama: {error}"
        )

        raise