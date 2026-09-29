from django.core.management.base import BaseCommand

from productos.models import Producto


class Command(BaseCommand):
    help = "Carga productos de demostración de la Librería Punto y Coma"

    def handle(self, *args, **options):

        productos = [
            {
                "codigo": "LIB001",
                "nombre": "El principito",
                "descripcion": (
                    "Novela corta de Antoine de Saint-Exupéry, "
                    "orientada a público juvenil y adulto."
                ),
                "categoria": "literatura",
                "precio": 45.00,
                "cantidad_existente": 12,
                "stock_minimo": 5,
                "estado": True,
            },
            {
                "codigo": "LIB002",
                "nombre": "Cien años de soledad",
                "descripcion": (
                    "Novela de Gabriel García Márquez, "
                    "representativa del realismo mágico."
                ),
                "categoria": "literatura",
                "precio": 85.00,
                "cantidad_existente": 3,
                "stock_minimo": 5,
                "estado": True,
            },
            {
                "codigo": "LIB003",
                "nombre": "Álgebra de Baldor",
                "descripcion": (
                    "Libro académico de álgebra utilizado "
                    "como material de apoyo educativo."
                ),
                "categoria": "academicos",
                "precio": 95.00,
                "cantidad_existente": 8,
                "stock_minimo": 4,
                "estado": True,
            },
            {
                "codigo": "LIB004",
                "nombre": "Don Quijote de la Mancha",
                "descripcion": (
                    "Obra clásica de la literatura española "
                    "escrita por Miguel de Cervantes."
                ),
                "categoria": "literatura",
                "precio": 120.00,
                "cantidad_existente": 2,
                "stock_minimo": 3,
                "estado": True,
            },
            {
                "codigo": "LIB005",
                "nombre": "Cuentos de la selva",
                "descripcion": (
                    "Colección de cuentos de Horacio Quiroga "
                    "dirigida principalmente al público infantil."
                ),
                "categoria": "infantil",
                "precio": 38.00,
                "cantidad_existente": 10,
                "stock_minimo": 4,
                "estado": True,
            },
            {
                "codigo": "PAP001",
                "nombre": "Cuaderno universitario",
                "descripcion": (
                    "Cuaderno universitario de 100 hojas "
                    "para uso escolar y académico."
                ),
                "categoria": "cuadernos",
                "precio": 18.00,
                "cantidad_existente": 35,
                "stock_minimo": 10,
                "estado": True,
            },
            {
                "codigo": "PAP002",
                "nombre": "Bolígrafo azul",
                "descripcion": (
                    "Bolígrafo de tinta azul para escritura "
                    "de uso escolar y de oficina."
                ),
                "categoria": "escritura",
                "precio": 4.00,
                "cantidad_existente": 50,
                "stock_minimo": 15,
                "estado": True,
            },
            {
                "codigo": "PAP003",
                "nombre": "Lápiz HB",
                "descripcion": (
                    "Lápiz de grafito HB para escritura "
                    "y dibujo escolar."
                ),
                "categoria": "escritura",
                "precio": 2.50,
                "cantidad_existente": 6,
                "stock_minimo": 10,
                "estado": True,
            },
            {
                "codigo": "PAP004",
                "nombre": "Marcadores de colores",
                "descripcion": (
                    "Paquete de marcadores de colores "
                    "para actividades escolares."
                ),
                "categoria": "escritura",
                "precio": 25.00,
                "cantidad_existente": 15,
                "stock_minimo": 5,
                "estado": True,
            },
            {
                "codigo": "OFI001",
                "nombre": "Resma de papel A4",
                "descripcion": (
                    "Resma de papel blanco tamaño A4 "
                    "para impresión y fotocopiado."
                ),
                "categoria": "oficina",
                "precio": 48.00,
                "cantidad_existente": 0,
                "stock_minimo": 5,
                "estado": True,
            },
            {
                "codigo": "OFI002",
                "nombre": "Archivador tamaño carta",
                "descripcion": (
                    "Archivador para organización de documentos "
                    "en formato tamaño carta."
                ),
                "categoria": "oficina",
                "precio": 22.00,
                "cantidad_existente": 7,
                "stock_minimo": 5,
                "estado": True,
            },
            {
                "codigo": "OFI003",
                "nombre": "Carpeta plástica",
                "descripcion": (
                    "Carpeta plástica para almacenar documentos "
                    "y material académico."
                ),
                "categoria": "oficina",
                "precio": 12.00,
                "cantidad_existente": 4,
                "stock_minimo": 8,
                "estado": True,
            },
        ]

        creados = 0
        existentes = 0

        self.stdout.write("")
        self.stdout.write("=" * 55)
        self.stdout.write("        LIBRERÍA PUNTO Y COMA")
        self.stdout.write("        CARGA DE DATOS DE DEMOSTRACIÓN")
        self.stdout.write("=" * 55)
        self.stdout.write("")

        for datos in productos:

            producto, creado = Producto.objects.get_or_create(
                codigo=datos["codigo"],
                defaults={
                    "nombre": datos["nombre"],
                    "descripcion": datos["descripcion"],
                    "categoria": datos["categoria"],
                    "precio": datos["precio"],
                    "cantidad_existente": datos["cantidad_existente"],
                    "stock_minimo": datos["stock_minimo"],
                    "estado": datos["estado"],
                },
            )

            if creado:
                creados += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"[+] {producto.codigo} - {producto.nombre}"
                    )
                )

            else:
                existentes += 1

                self.stdout.write(
                    self.style.WARNING(
                        f"[=] {producto.codigo} - "
                        f"{producto.nombre} ya existe"
                    )
                )

        self.stdout.write("")
        self.stdout.write("-" * 55)

        self.stdout.write(
            self.style.SUCCESS(
                f"Productos creados: {creados}"
            )
        )

        self.stdout.write(
            f"Productos existentes: {existentes}"
        )

        self.stdout.write(
            f"Total en la base de datos: "
            f"{Producto.objects.count()}"
        )

        self.stdout.write("-" * 55)

        self.stdout.write(
            self.style.SUCCESS(
                "Datos de demostración cargados correctamente."
            )
        )

        self.stdout.write("")