# Documentación técnica — Librería Punto y Coma

## 1. Descripción del proyecto

Librería Punto y Coma es una aplicación web desarrollada con Django para administrar el inventario de una librería.

El sistema permite gestionar productos mediante operaciones CRUD, controlar las existencias disponibles, realizar búsquedas, generar reportes y consultar la información almacenada utilizando inteligencia artificial local mediante Ollama.

La aplicación fue desarrollada como proyecto de Programación IV utilizando un entorno Linux MiniOS.

---

## 2. Objetivo

Desarrollar una aplicación web que integre:

- Gestión de productos mediante CRUD.
- Base de datos SQLite.
- Control de existencias.
- Búsqueda y filtrado de productos.
- Reportes de inventario.
- Chat basado en inteligencia artificial local.
- Restricción de consultas fuera del ámbito del inventario.
- Historial de consultas realizadas a la IA.
- Manejo de errores de comunicación con Ollama.

---

## 3. Tecnologías

| Tecnología | Uso |
|---|---|
| Python 3.11 | Lenguaje principal |
| Django 5.0.4 | Framework web |
| SQLite | Base de datos |
| Ollama | Ejecución local del modelo de IA |
| Qwen2.5 1.5B | Modelo base |
| productos-qwen2.5 | Modelo configurado para el proyecto |
| HTML5 | Estructura de la interfaz |
| CSS3 | Diseño visual |
| JavaScript | Interacciones de la interfaz |
| Git | Control de versiones |

---

## 4. Arquitectura general

El sistema utiliza la arquitectura proporcionada por Django basada en separación entre modelos, vistas y plantillas.

```text
Usuario
   |
   v
Interfaz web
   |
   v
Django
   |
   +-------------------+
   |                   |
   v                   v
Productos             Chat IA
   |                   |
   v                   +--> Validación de consulta
SQLite                 |
                       +--> Consulta del inventario
                       |
                       +--> Construcción del contexto
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

---

## 5. Aplicaciones Django

El proyecto se encuentra dividido principalmente en dos aplicaciones.

### productos

Responsable de:

- CRUD.
- Validaciones.
- Inventario.
- Búsquedas.
- Control de existencias.
- Reportes.
- Dashboard.
- Datos de demostración.

### chat

Responsable de:

- Comunicación con Ollama.
- Chat de inteligencia artificial.
- Restricción de consultas.
- Historial.
- Registro de respuestas.
- Manejo de errores de Ollama.

---

## 6. Modelo Producto

La entidad principal es `Producto`.

Los datos administrados son:

| Campo | Descripción |
|---|---|
| id | Identificador generado por Django |
| codigo | Código único del producto |
| nombre | Nombre |
| descripcion | Descripción |
| categoria | Categoría |
| precio | Precio |
| cantidad_existente | Cantidad disponible |
| stock_minimo | Existencia mínima recomendada |
| estado | Activo o inactivo |
| fecha_registro | Fecha de creación |

El sistema evita valores negativos donde corresponde y controla la unicidad del código.

---

## 7. Datos del negocio

Para representar un escenario real se seleccionó una librería ficticia denominada:

**Librería Punto y Coma**

El proyecto incluye productos de demostración correspondientes a:

- Literatura.
- Libros educativos.
- Papelería.
- Material de oficina.
- Otros productos relacionados con una librería.

Los datos pueden cargarse mediante:

```bash
python manage.py cargar_datos_demo
```

El comando verifica previamente la existencia de los productos para evitar duplicados.

---

## 8. Base de datos

Durante el desarrollo se utiliza SQLite.

La base puede reconstruirse ejecutando:

```bash
python manage.py migrate
```

Posteriormente se cargan los datos iniciales:

```bash
python manage.py cargar_datos_demo
```

Esto evita depender de una copia específica de `db.sqlite3` para desplegar el proyecto.

---

## 9. CRUD

La aplicación implementa las operaciones:

### Crear

Permite registrar productos nuevos.

### Leer

Permite visualizar:

- Lista de productos.
- Detalle individual.
- Búsquedas.
- Filtros.

### Actualizar

Permite modificar los datos existentes.

### Eliminar

Permite eliminar o gestionar los productos de acuerdo con la lógica implementada en el sistema.

Las operaciones utilizan formularios Django para validar la información antes de almacenarla.

---

## 10. Reportes

El módulo de reportes permite consultar información procesada directamente desde SQLite.

Entre los reportes implementados se encuentran:

1. Todos los productos.
2. Producto más caro.
3. Producto más barato.
4. Productos con pocas existencias.
5. Productos agotados.
6. Productos por categoría.
7. Valor total del inventario.
8. Productos con mayor cantidad disponible.

El cálculo de los reportes se realiza utilizando consultas del ORM de Django.

---

## 11. Integración con Ollama

Ollama se ejecuta localmente.

La aplicación se comunica con:

```text
http://127.0.0.1:11434
```

El modelo base utilizado es:

```text
qwen2.5:1.5b
```

A partir del modelo base se creó:

```text
productos-qwen2.5
```

mediante:

```bash
ollama create productos-qwen2.5 -f ollama/Modelfile-productos
```

---

## 12. Flujo de una consulta de IA

El procesamiento general es:

```text
Pregunta
   |
   v
Django
   |
   v
Validación
   |
   +-- fuera de ámbito --> rechazo
   |
   v
Consulta de productos
   |
   v
Contexto estructurado
   |
   v
Ollama
   |
   v
Respuesta
   |
   v
Registro en historial
```

Django obtiene los productos registrados y proporciona a Ollama la información necesaria para responder.

---

## 13. Restricciones

Se aplican restricciones para evitar que el asistente sea utilizado como un chatbot general.

El sistema utiliza dos niveles de control.

### Restricción desde Django

Antes de enviar determinadas consultas a Ollama, Django comprueba que correspondan al dominio permitido.

Una consulta ajena al inventario puede devolver:

```text
Solo puedo responder consultas sobre productos y sus atributos.
```

### Restricción mediante Modelfile

El archivo:

```text
ollama/Modelfile-productos
```

contiene instrucciones para orientar el modelo hacia productos e inventario.

La validación desde Django constituye una capa adicional de control y evita depender únicamente del comportamiento probabilístico del modelo.

---

## 14. Historial de inteligencia artificial

Las consultas realizadas se almacenan mediante el modelo `ConsultaIA`.

Se registra información como:

- Pregunta.
- Respuesta.
- Fecha.
- Modelo utilizado.
- Resultado.

Las consultas pueden clasificarse como:

```text
Procesada por IA
Rechazada por ámbito
Error de Ollama
```

Esto permite conservar evidencia textual de las pruebas realizadas con la inteligencia artificial.

---

## 15. Manejo de errores

La aplicación contempla el caso en que Ollama no se encuentre disponible.

En lugar de detener completamente la aplicación, Django captura el problema y muestra un mensaje adecuado.

De esta forma, la gestión normal del inventario puede mantenerse separada del servicio de inteligencia artificial.

---

## 16. Variables de entorno

La configuración dependiente del equipo no se encuentra fijada directamente en el código.

Se utiliza `.env` para valores locales y `.env.example` como plantilla distribuible.

Ejemplo:

```env
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,IP_DE_LA_MAQUINA
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=productos-qwen2.5
```

El archivo `.env` se excluye mediante `.gitignore`.

---

## 17. Acceso mediante red local

Django puede ejecutarse escuchando en todas las interfaces:

```bash
python manage.py runserver 0.0.0.0:8000
```

Desde otro equipo perteneciente a una red accesible puede utilizarse:

```text
http://IP_DEL_SERVIDOR:8000/
```

La IP correspondiente debe encontrarse permitida mediante `DJANGO_ALLOWED_HOSTS`.

---

## 18. Interfaz

La interfaz fue diseñada específicamente para el contexto de Librería Punto y Coma.

Incluye navegación hacia:

- Dashboard.
- Productos.
- Reportes.
- Chat IA.
- Historial.

Se buscó mantener una interfaz clara, consistente y adecuada para un sistema básico de administración de inventario.

---

## 19. Decisiones técnicas

### SQLite

Se seleccionó por ser suficiente para el alcance académico del proyecto, no requerir un servidor adicional y facilitar el despliegue.

### Ollama

Permite ejecutar el modelo de IA localmente sin depender de una API de inteligencia artificial en la nube.

### Qwen2.5 1.5B

Se seleccionó un modelo pequeño debido a los recursos disponibles en el entorno MiniOS.

### Django ORM

Las consultas del inventario se realizan mediante el ORM de Django para evitar escribir directamente SQL en las operaciones normales del sistema.

### Variables de entorno

La dirección de Ollama, modelo y hosts permitidos se separaron del código fuente para facilitar el despliegue en otros equipos.

### Datos reproducibles

Los datos iniciales pueden reconstruirse mediante `cargar_datos_demo` en lugar de depender exclusivamente de una base SQLite previamente creada.

---

## 20. Estructura de archivos principales

```text
proyecto/
|
+-- chat/
|   +-- models.py
|   +-- views.py
|   +-- ollama_api.py
|   +-- templates/
|
+-- productos/
|   +-- models.py
|   +-- forms.py
|   +-- views.py
|   +-- urls.py
|   +-- management/
|   +-- templates/
|
+-- chatapp/
|   +-- settings.py
|   +-- urls.py
|
+-- ollama/
|   +-- Modelfile-productos
|
+-- manage.py
+-- requirements.txt
+-- .env.example
+-- README.md
+-- DOCUMENTACION.md
```

---

## 21. Despliegue

Las instrucciones completas se encuentran en:

```text
README.md
```

El proceso general consiste en:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env

python manage.py migrate
python manage.py cargar_datos_demo

ollama pull qwen2.5:1.5b
ollama create productos-qwen2.5 -f ollama/Modelfile-productos

python manage.py runserver 0.0.0.0:8000
```

---

## 22. Limitaciones

El proyecto fue diseñado como una aplicación académica.

Entre sus limitaciones se encuentran:

- SQLite no está orientado a cargas empresariales grandes.
- El servidor `runserver` de Django se utiliza únicamente para desarrollo y demostración.
- Las respuestas dependen de las capacidades del modelo local seleccionado.
- Un modelo pequeño puede interpretar incorrectamente preguntas ambiguas.
- Las restricciones mediante instrucciones de un modelo generativo no constituyen por sí solas un mecanismo de seguridad absoluto.
- El sistema no implementa ventas, facturación ni compras.
- El sistema no pretende sustituir un sistema comercial completo de gestión empresarial.

---

## 23. Conclusión técnica

El proyecto demuestra la integración de una aplicación web tradicional basada en Django y SQLite con un modelo de inteligencia artificial ejecutado localmente mediante Ollama.

La separación entre la gestión de productos, las consultas del inventario y el módulo de inteligencia artificial permite mantener una estructura comprensible y facilita su despliegue.

El uso de datos reproducibles, variables de entorno, restricciones de consultas e historial permite presentar un sistema funcional acorde con el alcance definido para Librería Punto y Coma.
