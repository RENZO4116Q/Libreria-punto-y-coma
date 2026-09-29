from django.contrib import messages
from django.db.models import Q, F, Sum, DecimalField, ExpressionWrapper
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ProductoForm
from .models import Producto


def dashboard(request):

    productos = Producto.objects.all()
    productos_activos = productos.filter(estado=True)

    total_productos = productos.count()
    total_activos = productos_activos.count()

    productos_agotados = productos_activos.filter(
        cantidad_existente=0
    )

    productos_stock_bajo = productos_activos.filter(
        cantidad_existente__gt=0,
        cantidad_existente__lte=F("stock_minimo"),
    )

    valor_total = productos_activos.aggregate(
        total=Sum(
            ExpressionWrapper(
                F("precio") * F("cantidad_existente"),
                output_field=DecimalField(
                    max_digits=14,
                    decimal_places=2,
                ),
            )
        )
    )["total"] or 0

    ultimos_productos = productos.order_by(
        "-fecha_registro"
    )[:5]

    contexto = {
        "total_productos": total_productos,
        "total_activos": total_activos,
        "total_stock_bajo": productos_stock_bajo.count(),
        "total_agotados": productos_agotados.count(),
        "valor_total": valor_total,
        "productos_stock_bajo": productos_stock_bajo[:5],
        "productos_agotados": productos_agotados[:5],
        "ultimos_productos": ultimos_productos,
    }

    return render(
        request,
        "productos/dashboard.html",
        contexto,
    )


def lista_productos(request):

    productos = Producto.objects.all()

    busqueda = request.GET.get("q", "").strip()
    categoria = request.GET.get("categoria", "").strip()
    estado_stock = request.GET.get("stock", "").strip()

    if busqueda:
        productos = productos.filter(
            Q(codigo__icontains=busqueda)
            | Q(nombre__icontains=busqueda)
            | Q(descripcion__icontains=busqueda)
        )

    if categoria:
        productos = productos.filter(
            categoria=categoria
        )

    if estado_stock == "agotado":
        productos = productos.filter(
            cantidad_existente=0
        )

    elif estado_stock == "bajo":
        from django.db.models import F

        productos = productos.filter(
            cantidad_existente__gt=0,
            cantidad_existente__lte=F("stock_minimo"),
        )

    elif estado_stock == "normal":
        from django.db.models import F

        productos = productos.filter(
            cantidad_existente__gt=F("stock_minimo")
        )

    contexto = {
        "productos": productos,
        "busqueda": busqueda,
        "categoria_seleccionada": categoria,
        "stock_seleccionado": estado_stock,
        "categorias": Producto.Categoria.choices,
    }

    return render(
        request,
        "productos/lista.html",
        contexto,
    )


def detalle_producto(request, pk):

    producto = get_object_or_404(
        Producto,
        pk=pk,
    )

    return render(
        request,
        "productos/detalle.html",
        {
            "producto": producto,
        },
    )


def crear_producto(request):

    if request.method == "POST":
        formulario = ProductoForm(request.POST)

        if formulario.is_valid():
            producto = formulario.save()

            messages.success(
                request,
                f"El producto {producto.nombre} "
                "fue registrado correctamente.",
            )

            return redirect(
                "productos:detalle",
                pk=producto.pk,
            )

    else:
        formulario = ProductoForm()

    return render(
        request,
        "productos/formulario.html",
        {
            "formulario": formulario,
            "titulo": "Registrar producto",
            "texto_boton": "Guardar producto",
        },
    )


def editar_producto(request, pk):

    producto = get_object_or_404(
        Producto,
        pk=pk,
    )

    if request.method == "POST":

        formulario = ProductoForm(
            request.POST,
            instance=producto,
        )

        if formulario.is_valid():

            producto = formulario.save()

            messages.success(
                request,
                f"El producto {producto.nombre} "
                "fue actualizado correctamente.",
            )

            return redirect(
                "productos:detalle",
                pk=producto.pk,
            )

    else:
        formulario = ProductoForm(
            instance=producto
        )

    return render(
        request,
        "productos/formulario.html",
        {
            "formulario": formulario,
            "producto": producto,
            "titulo": "Editar producto",
            "texto_boton": "Guardar cambios",
        },
    )


def eliminar_producto(request, pk):

    producto = get_object_or_404(
        Producto,
        pk=pk,
    )

    if request.method == "POST":

        nombre = producto.nombre

        producto.delete()

        messages.success(
            request,
            f"El producto {nombre} "
            "fue eliminado correctamente.",
        )

        return redirect(
            "productos:lista"
        )

    return render(
        request,
        "productos/eliminar.html",
        {
            "producto": producto,
        },
    )


def reportes(request):

    productos = Producto.objects.filter(estado=True)

    # -------------------------------------------------
    # 1. TODOS LOS PRODUCTOS
    # -------------------------------------------------

    todos_productos = productos.order_by("nombre")


    # -------------------------------------------------
    # 2. PRODUCTO MÁS CARO
    # -------------------------------------------------

    producto_mas_caro = productos.order_by(
        "-precio"
    ).first()


    # -------------------------------------------------
    # 3. PRODUCTO MÁS BARATO
    # -------------------------------------------------

    producto_mas_barato = productos.order_by(
        "precio"
    ).first()


    # -------------------------------------------------
    # 4. PRODUCTOS CON STOCK BAJO
    # -------------------------------------------------

    stock_bajo = productos.filter(
        cantidad_existente__gt=0,
        cantidad_existente__lte=F("stock_minimo"),
    ).order_by("cantidad_existente")


    # -------------------------------------------------
    # 5. PRODUCTOS AGOTADOS
    # -------------------------------------------------

    agotados = productos.filter(
        cantidad_existente=0
    ).order_by("nombre")


    # -------------------------------------------------
    # 6. PRODUCTOS POR CATEGORÍA
    # -------------------------------------------------

    categoria_seleccionada = request.GET.get(
        "categoria",
        ""
    )

    productos_categoria = Producto.objects.none()

    if categoria_seleccionada:

        productos_categoria = productos.filter(
            categoria=categoria_seleccionada
        ).order_by("nombre")


    # -------------------------------------------------
    # 7. VALOR TOTAL DEL INVENTARIO
    # -------------------------------------------------

    valor_total = productos.aggregate(
        total=Sum(
            ExpressionWrapper(
                F("precio") * F("cantidad_existente"),
                output_field=DecimalField(
                    max_digits=14,
                    decimal_places=2,
                ),
            )
        )
    )["total"] or 0


    # -------------------------------------------------
    # 8. PRODUCTOS CON MAYOR EXISTENCIA
    # -------------------------------------------------

    mayor_existencia = productos.order_by(
        "-cantidad_existente",
        "nombre"
    )[:5]


    contexto = {

        "todos_productos": todos_productos,

        "producto_mas_caro": producto_mas_caro,

        "producto_mas_barato": producto_mas_barato,

        "stock_bajo": stock_bajo,

        "agotados": agotados,

        "categorias": Producto._meta.get_field("categoria").choices,

        "categoria_seleccionada": categoria_seleccionada,

        "productos_categoria": productos_categoria,

        "valor_total": valor_total,

        "mayor_existencia": mayor_existencia,

    }

    return render(
        request,
        "productos/reportes.html",
        contexto,
    )

@require_POST
def aumentar_stock(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    producto.cantidad_existente += 1
    producto.save()

    messages.success(
        request,
        f"Se aumentó el stock de {producto.nombre}. "
        f"Existencia actual: {producto.cantidad_existente}."
    )

    return redirect(
        "productos:detalle",
        pk=producto.pk
    )


@require_POST
def disminuir_stock(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if producto.cantidad_existente <= 0:

        messages.error(
            request,
            f"No se puede disminuir el stock de {producto.nombre} "
            "porque ya está agotado."
        )

    else:

        producto.cantidad_existente -= 1
        producto.save()

        messages.success(
            request,
            f"Se disminuyó el stock de {producto.nombre}. "
            f"Existencia actual: {producto.cantidad_existente}."
        )

    return redirect(
        "productos:detalle",
        pk=producto.pk
    )