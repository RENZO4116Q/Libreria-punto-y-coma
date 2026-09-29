from django import forms

from .models import Producto


class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto

        fields = [
            "codigo",
            "nombre",
            "descripcion",
            "categoria",
            "precio",
            "cantidad_existente",
            "stock_minimo",
            "estado",
        ]

        widgets = {
            "codigo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: LIB006",
                }
            ),

            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre del producto",
                }
            ),

            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Descripción del producto",
                }
            ),

            "categoria": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "precio": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01",
                }
            ),

            "cantidad_existente": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                }
            ),

            "stock_minimo": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                }
            ),

            "estado": forms.CheckboxInput(
                attrs={
                    "class": "form-check",
                }
            ),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data["codigo"].strip().upper()

        consulta = Producto.objects.filter(codigo__iexact=codigo)

        if self.instance.pk:
            consulta = consulta.exclude(pk=self.instance.pk)

        if consulta.exists():
            raise forms.ValidationError(
                "Ya existe otro producto con este código."
            )

        return codigo

    def clean_precio(self):
        precio = self.cleaned_data["precio"]

        if precio < 0:
            raise forms.ValidationError(
                "El precio no puede ser negativo."
            )

        return precio

    def clean_cantidad_existente(self):
        cantidad = self.cleaned_data["cantidad_existente"]

        if cantidad < 0:
            raise forms.ValidationError(
                "La cantidad existente no puede ser negativa."
            )

        return cantidad

    def clean_stock_minimo(self):
        stock = self.cleaned_data["stock_minimo"]

        if stock < 0:
            raise forms.ValidationError(
                "El stock mínimo no puede ser negativo."
            )

        return stock