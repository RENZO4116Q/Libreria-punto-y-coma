# Librería Punto y Coma

Sistema web de gestión de inventario desarrollado con Django e integrado con inteligencia artificial local mediante Ollama.

El proyecto permite administrar los productos de una librería mediante operaciones CRUD, controlar existencias, generar reportes y realizar consultas en lenguaje natural sobre el inventario utilizando un modelo local de inteligencia artificial.

---

# 1. Tecnologías utilizadas

- Python 3.11
- Django 5.0.4
- SQLite
- Ollama
- Qwen2.5 1.5B
- HTML5
- CSS3
- JavaScript

---

# 2. Funcionalidades

## Gestión de productos

El sistema permite:

- Registrar productos.
- Consultar productos.
- Editar productos.
- Eliminar o desactivar productos.
- Buscar por código.
- Buscar por nombre.
- Buscar por categoría.
- Controlar cantidades disponibles.
- Detectar productos agotados.
- Detectar productos con stock bajo.

Cada producto contiene:

- Código.
- Nombre.
- Descripción.
- Categoría.
- Precio.
- Cantidad existente.
- Stock mínimo.
- Estado.
- Fecha de registro.

## Reportes

El sistema incluye los siguientes reportes:

1. Todos los productos.
2. Producto más caro.
3. Producto más barato.
4. Productos con pocas existencias.
5. Productos agotados.
6. Productos por categoría.
7. Valor total del inventario.
8. Productos con mayor cantidad disponible.

## Inteligencia artificial

El sistema integra Ollama para realizar consultas sobre los productos almacenados en SQLite.

El flujo utilizado es:

```text
Usuario
   |
   v
Django
   |
   +--> Validación de la pregunta
   |
   +--> Consulta SQLite
   |
   +--> Preparación del inventario
   |
   v
Ollama
   |
   v
productos-qwen2.5
   |
   v
Respuesta
```

El sistema incorpora validaciones desde Django para impedir consultas ajenas al inventario.

## Historial de IA

Las consultas realizadas son almacenadas en la base de datos.

El historial permite distinguir entre:

- Procesada por IA.
- Rechazada por ámbito.
- Error de Ollama.

Se almacenan:

- Pregunta.
- Respuesta.
- Fecha y hora.
- Modelo utilizado.
- Resultado de la consulta.

---

# 3. Estructura del proyecto

```text
ollama-django/
|
+-- chat/
|   +-- migrations/
|   +-- templates/
|   |   +-- chat.html
|   |   +-- historial.html
|   +-- models.py
|   +-- ollama_api.py
|   +-- views.py
|
+-- chatapp/
|   +-- settings.py
|   +-- urls.py
|   +-- asgi.py
|   +-- wsgi.py
|
+-- productos/
|   +-- management/
|   |   +-- commands/
|   |       +-- cargar_datos_demo.py
|   +-- migrations/
|   +-- templates/
|   |   +-- productos/
|   +-- forms.py
|   +-- models.py
|   +-- urls.py
|   +-- views.py
|
+-- ollama/
|   +-- Modelfile-productos
|
+-- .env.example
+-- requirements.txt
+-- manage.py
+-- README.md
```

---

# 4. Requisitos

Para ejecutar el proyecto se necesita:

- Linux, MiniOS u otro sistema compatible con Python.
- Python 3.11 o superior compatible.
- pip.
- Git.
- Ollama.

Comprobar Python:

```bash
python3 --version
```

Comprobar pip:

```bash
pip3 --version
```

Comprobar Git:

```bash
git --version
```

Comprobar Ollama:

```bash
ollama --version
```

---

# 5. Instalación

## 5.1 Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
cd libreria-punto-y-coma
```

---

## 5.2 Crear entorno virtual

```bash
python3 -m venv venv
```

Activarlo:

```bash
source venv/bin/activate
```

---

## 5.3 Instalar dependencias

```bash
pip install -r requirements.txt
```

Las principales dependencias son:

```text
Django==5.0.4
ollama==0.6.2
python-dotenv==1.0.1
```

---

# 6. Configuración

Crear el archivo `.env` utilizando el ejemplo:

```bash
cp .env.example .env
```

Editar:

```bash
nano .env
```

Ejemplo:

```env
DJANGO_DEBUG=True

DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0,IP_DE_LA_MAQUINA

OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=productos-qwen2.5
```

Para acceder desde otro equipo de la red se debe agregar la dirección IP del servidor Django en `DJANGO_ALLOWED_HOSTS`.

---

# 7. Preparar la base de datos

Ejecutar las migraciones:

```bash
python manage.py migrate
```

Comprobarlas:

```bash
python manage.py showmigrations
```

---

# 8. Cargar datos de demostración

El proyecto incluye un comando para cargar productos de la Librería Punto y Coma:

```bash
python manage.py cargar_datos_demo
```

El comando puede ejecutarse nuevamente sin duplicar los productos existentes.

Para comprobar los datos:

```bash
python manage.py shell
```

Dentro del shell:

```python
from productos.models import Producto

Producto.objects.count()
Producto.objects.all()
```

Salir:

```python
exit()
```

---

# 9. Configurar Ollama

Comprobar que Ollama esté disponible:

```bash
curl http://127.0.0.1:11434/api/tags
```

Consultar modelos:

```bash
ollama list
```

Descargar el modelo base:

```bash
ollama pull qwen2.5:1.5b
```

---

# 10. Crear el modelo especializado

El proyecto contiene:

```text
ollama/Modelfile-productos
```

Crear el modelo:

```bash
ollama create productos-qwen2.5 -f ollama/Modelfile-productos
```

Comprobar:

```bash
ollama list
```

Debe aparecer:

```text
productos-qwen2.5:latest
```

El modelo puede probarse mediante:

```bash
ollama run productos-qwen2.5
```

Para salir:

```text
/bye
```

---

# 11. Restricciones de inteligencia artificial

El sistema utiliza dos niveles principales de control.

## Nivel 1 - Django

Django valida las consultas antes de enviarlas al modelo.

Una pregunta ajena al inventario puede ser rechazada directamente con:

```text
Solo puedo responder consultas sobre productos y sus atributos.
```

## Nivel 2 - Ollama

El archivo:

```text
ollama/Modelfile-productos
```

define instrucciones adicionales para especializar el comportamiento del modelo.

La aplicación no depende exclusivamente de las instrucciones del modelo para aplicar las restricciones.

---

# 12. Ejecutar el sistema

Ejecutar:

```bash
python manage.py runserver 0.0.0.0:8000
```

Desde la misma máquina:

```text
http://127.0.0.1:8000/
```

Desde otro equipo de la red:

```text
http://IP_DEL_SERVIDOR:8000/
```

Ejemplo:

```text
http://192.168.0.110:8000/
```

---

# 13. Rutas principales

```text
/                       Dashboard
/productos/              Productos
/productos/reportes/     Reportes
/chat/                   Asistente IA
/historial/              Historial de IA
```

---

# 14. Pruebas recomendadas

## CRUD

Registrar un producto nuevo y comprobar:

- Código único.
- Precio no negativo.
- Cantidad no negativa.
- Edición.
- Eliminación o desactivación.

## Reportes

Comprobar:

- Producto más caro.
- Producto más barato.
- Stock bajo.
- Productos agotados.
- Categorías.
- Valor total del inventario.

## Inteligencia artificial

Ejemplo:

```text
¿Cuál es el producto más caro?
```

```text
¿Qué productos tienen pocas existencias?
```

```text
¿Qué productos están agotados?
```

```text
¿Cuál es el valor total del inventario?
```

## Restricción

Probar:

```text
¿Cuál es la capital de Francia?
```

La aplicación debe rechazar la consulta por encontrarse fuera del ámbito del inventario.

## Historial

Ingresar en:

```text
/historial/
```

y comprobar que las consultas realizadas hayan sido almacenadas.

---

# 15. Solución de problemas

## Ollama no responde

Comprobar:

```bash
curl http://127.0.0.1:11434/api/tags
```

y:

```bash
ollama list
```

## El modelo no existe

Ejecutar:

```bash
ollama pull qwen2.5:1.5b
ollama create productos-qwen2.5 -f ollama/Modelfile-productos
```

## Error de Django por host

Agregar la IP correspondiente en `.env`:

```env
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,IP_DEL_SERVIDOR
```

Reiniciar Django.

## Base de datos vacía

Ejecutar:

```bash
python manage.py migrate
python manage.py cargar_datos_demo
```

---

# 16. Comandos de ejecución rápida

En una instalación ya configurada:

```bash
cd ~/ollama-django

source venv/bin/activate

python manage.py check

python manage.py runserver 0.0.0.0:8000
```

Comprobar Ollama en otra terminal:

```bash
ollama list
```

---

# 17. Autor

Proyecto desarrollado como Entregable Final de Programación IV.

Aplicación: **Librería Punto y Coma**

Tecnologías principales: **Django + SQLite + Ollama**
