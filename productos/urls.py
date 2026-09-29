from django.urls import path

from . import views


app_name = "productos"


urlpatterns = [
    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),
    path(
        "",
        views.lista_productos,
        name="lista",
    ),

    path(
        "nuevo/",
        views.crear_producto,
        name="crear",
    ),

    path(
        "<int:pk>/",
        views.detalle_producto,
        name="detalle",
    ),

    path(
        "<int:pk>/editar/",
        views.editar_producto,
        name="editar",
    ),

    path(
        "<int:pk>/eliminar/",
        views.eliminar_producto,
        name="eliminar",
    ),
        path(
        "reportes/",
        views.reportes,
        name="reportes",
    ),
    path(
        "<int:pk>/stock/aumentar/",
        views.aumentar_stock,
        name="aumentar_stock",
    ),

    path(
        "<int:pk>/stock/disminuir/",
        views.disminuir_stock,
        name="disminuir_stock",
    ),
]