from django.core.validators import MinValueValidator
from django.db import models


class Producto(models.Model):

    class Categoria(models.TextChoices):
        LITERATURA = "literatura", "Literatura"
        ACADEMICOS = "academicos", "Académicos"
        INFANTIL = "infantil", "Infantil"
        CUADERNOS = "cuadernos", "Cuadernos"
        ESCRITURA = "escritura", "Escritura"
        OFICINA = "oficina", "Oficina"
        OTROS = "otros", "Otros"

    codigo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Código",
    )

    nombre = models.CharField(
        max_length=150,
        verbose_name="Nombre",
    )

    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción",
    )

    categoria = models.CharField(
        max_length=30,
        choices=Categoria.choices,
        default=Categoria.OTROS,
        verbose_name="Categoría",
    )

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Precio",
    )

    cantidad_existente = models.PositiveIntegerField(
        default=0,
        verbose_name="Cantidad existente",
    )

    stock_minimo = models.PositiveIntegerField(
        default=0,
        verbose_name="Stock mínimo",
    )

    estado = models.BooleanField(
        default=True,
        verbose_name="Activo",
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de registro",
    )

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    @property
    def agotado(self):
        return self.cantidad_existente == 0

    @property
    def stock_bajo(self):
        return (
            self.cantidad_existente > 0
            and self.cantidad_existente <= self.stock_minimo
        )

    @property
    def valor_inventario(self):
        return self.precio * self.cantidad_existente
