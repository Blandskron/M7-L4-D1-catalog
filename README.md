# Evolución Controlada de un Catálogo de Productos (Django)

Proyecto Django orientado a **controlar, versionar y reproducir la evolución del esquema de base de datos** utilizando el sistema de **migraciones** del framework.  
El foco no está en la interfaz ni en la lógica de negocio compleja, sino en **cómo el modelo de datos cambia de forma progresiva, segura y trazable**, tal como ocurre en entornos reales de trabajo con equipos y múltiples despliegues.

---

## Objetivo del proyecto

Demostrar, de forma práctica y profesional, cómo Django resuelve el problema del **versionado del esquema de base de datos**, permitiendo:

- Evolucionar modelos sin perder datos
- Mantener sincronizados distintos entornos
- Registrar cada cambio estructural como un paso auditable
- Reproducir el estado exacto del esquema en cualquier momento

---

## Problema que resuelven las migraciones

En un proyecto real, el esquema de base de datos **no es estático**:

- Se agregan campos
- Se cambian tipos de datos
- Se definen valores por defecto
- Se renombran columnas
- Se ajustan reglas de negocio

Sin un sistema de migraciones, estos cambios:
- son difíciles de coordinar
- generan inconsistencias entre entornos
- provocan errores difíciles de rastrear
- rompen despliegues

Las migraciones de Django actúan como un **sistema de control de versiones del esquema**, equivalente a Git pero aplicado a la base de datos.

---

## Qué es una migración en Django

Una migración es un **archivo ejecutable y versionado** que describe **cómo pasar de un estado del esquema a otro**.

Cada migración:
- depende de una anterior
- define operaciones explícitas
- puede aplicarse o revertirse
- queda registrada en la base de datos

Django mantiene una tabla interna (`django_migrations`) donde guarda qué migraciones ya fueron ejecutadas.

---

## Estructura del proyecto relevante

```text
catalog/
├── admin.py
├── models.py
├── views.py
└── migrations/
├── 0001_initial.py
    ├── 0002_add_description_and_status.py
    ├── 0003_change_price_to_decimal.py
    └── 0004_rename_price_field.py
```

Solo estos archivos son relevantes para el objetivo del proyecto.

---

## Ciclo de evolución del esquema

> Nota didáctica: esta secuencia está pensada para inicializar una base de datos nueva. En un sistema que ya tiene `0001_initial` aplicada y compartida, no se reescriben migraciones publicadas; se crea una migración nueva con `makemigrations`.

### 1. Estado inicial del modelo

* Producto con SKU, nombre y precio entero
* Tabla base creada mediante `0001_initial.py`

```bash
python manage.py makemigrations
python manage.py migrate
```

Resultado: esquema mínimo, funcional y estable.

---

### 2. Agregar nuevos campos

Evolución del modelo:

* Se agrega `description`
* Se agrega `is_active` con valor por defecto

Motivo:

* Nuevos requerimientos sin romper datos existentes

Migración generada:

* `0002_add_description_and_status.py`

Este paso demuestra cómo Django:

* agrega columnas
* define defaults
* mantiene compatibilidad hacia atrás

---

### 3. Cambio de tipo de dato

Evolución del modelo:

* `price` pasa de `IntegerField` a `DecimalField`

Motivo:

* precisión monetaria real
* corrección de una decisión inicial simplificada

Migración generada:

* `0003_change_price_to_decimal.py`

Este paso refleja una situación real:
una decisión técnica madura reemplaza una solución inicial.

---

### 4. Renombrado semántico de columna

Evolución del modelo:

* `price` → `unit_price`

Motivo:

* claridad de dominio
* mejora semántica sin cambiar la estructura lógica

Migración generada:

* `0004_rename_price_field.py`

Django realiza el renombrado **sin recrear la tabla**, preservando datos.

---

## Uso de `makemigrations`

El comando:

```bash
python manage.py makemigrations
```

Hace lo siguiente:

* compara el estado actual de `models.py`
* contra el estado conocido por las migraciones
* genera un nuevo archivo que describe **solo la diferencia**

No modifica la base de datos.

En este proyecto, después de modificar `catalog/models.py`, el flujo correcto es:

```bash
python manage.py makemigrations catalog
python manage.py migrate
```

Para revisar que el modelo y los archivos de migración siguen sincronizados sin crear archivos:

```bash
python manage.py makemigrations --check --dry-run
```

---

## Uso de `migrate`

El comando:

```bash
python manage.py migrate
```

Hace lo siguiente:

* revisa qué migraciones no se han aplicado
* las ejecuta en orden
* registra cada ejecución

Este comando es el que **sincroniza el esquema real** con el modelo.

---

## Aplicación de migraciones existentes

Cuando un entorno nuevo se levanta desde cero:

```bash
python manage.py migrate
```

Django:

* ejecuta **todas** las migraciones en orden
* recrea el estado final del esquema
* sin necesidad de scripts manuales

También se puede inspeccionar el historial y el SQL previsto antes de aplicarlo:

```bash
python manage.py showmigrations catalog
python manage.py sqlmigrate catalog 0004
```

Esto garantiza:

* reproducibilidad
* consistencia
* despliegues confiables

---

## Ejecución con Docker

El proyecto incluye una configuración reproducible con PostgreSQL y Django:

* `Dockerfile`: construye la imagen de la aplicación.
* `.dockerignore`: excluye secretos, cachés y archivos locales del contexto de construcción.
* `docker-compose.yml`: inicia los servicios `db` (PostgreSQL) y `web` (Django).
* `docker-entrypoint.sh`: aplica las migraciones existentes, recopila estáticos y crea un superusuario de forma idempotente.

1. Copia la configuración de ejemplo y cambia, como mínimo, la contraseña y la clave secreta:

```bash
cp .env.example .env
```

En PowerShell:

```powershell
Copy-Item .env.example .env
```

2. Inicia el entorno:

```bash
docker compose up --build
```

Al arrancar, el contenedor `web` ejecuta `python manage.py migrate --noinput`. Por tanto, aplica tanto las migraciones de Django incluidas como las de `catalog`, en orden, y no necesita scripts SQL manuales.

El administrador se crea solo la primera vez con estas variables del archivo `.env`:

```text
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=change-this-password
```

Si ese usuario ya existe, el script no lo duplica ni modifica su contraseña. Accede a `http://localhost:8000/admin/` y al endpoint de comprobación `http://localhost:8000/api/catalog/`.

Para detener los servicios conservando la base de datos:

```bash
docker compose down
```

Para reconstruir la base de datos desde las migraciones (elimina el volumen y sus datos):

```bash
docker compose down -v
docker compose up --build
```

---

## Comentarios de base de datos (`db_comment`)

El proyecto utiliza `db_comment` en los campos del modelo para:

* documentar el esquema directamente en la base de datos
* mejorar trazabilidad
* facilitar mantenimiento

Ejemplo:

```python
unit_price = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    db_comment="Precio unitario con precisión decimal"
)
```

En PostgreSQL esto se traduce a comentarios reales a nivel de columna.

---

## Validación del esquema

* `admin.py` permite verificar visualmente el estado del modelo
* `views.py` fuerza consultas ORM para validar coherencia
* las migraciones garantizan que el esquema sea consistente
