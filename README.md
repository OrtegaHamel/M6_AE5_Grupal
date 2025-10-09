# 🗓️ Plataforma de Gestión de Eventos - Proyecto Grupal Django

## 📘 Contexto del Proyecto

Este proyecto corresponde a la **Evaluación M6_AE5** del módulo de Django, cuyo objetivo es desarrollar una **Plataforma de Gestión de Eventos** utilizando el **framework Django**.  

La aplicación permite a los usuarios **registrarse, iniciar sesión y gestionar eventos** como conferencias, conciertos o seminarios.  
Además, se implementa un sistema de **roles y permisos** para controlar el acceso a las distintas funcionalidades según el tipo de usuario.

---

## ⚙️ Objetivos Generales

- Configurar el sistema de **autenticación y autorización** de Django.
- Implementar un **control de acceso basado en roles**.
- Aplicar **mixins** y **mensajes de error** para mejorar la experiencia del usuario.
- Asegurar la correcta configuración de rutas y permisos en el proyecto.

---

## 🧩 Funcionalidades Principales

### 🔐 Sistema de Autenticación
- Registro de usuarios nuevos.
- Inicio y cierre de sesión.
- Restricción de acceso a las vistas según autenticación.

### 👤 Roles y Permisos
El sistema define **tres tipos de usuarios** con distintos niveles de acceso:

| Rol | Permisos |
|------|-----------|
| **Administrador** | Crear, editar y eliminar eventos. |
| **Organizador** | Crear y gestionar eventos propios, sin eliminarlos. |
| **Asistente** | Ver eventos a los que está registrado. |

> Los permisos se gestionan utilizando el **modelo `auth_permission`** de Django.

### Usuarios de prueba

``` bash
# Asistente (sin acceso al admin)
    username='asistente',
    password='contrasena123',
    is_staff=False  # Por defecto ya es False

# Organizador (con acceso al admin si es necesario)
    username='organizador',
    password='contrasena123',
    is_staff=True  # Solo si necesita acceso al admin

# Administrador
    username='administrador',
    password='contrasena123',
    is_staff=True,

```

### 🧱 Mixins y Control de Acceso
- Se utiliza **`LoginRequiredMixin`** para restringir acceso a vistas que requieren autenticación.
- Se aplica **`PermissionRequiredMixin`** para restringir la edición y eliminación de eventos a los usuarios con permisos adecuados.
- Se implementa una **vista personalizada de acceso denegado** para usuarios no autorizados.

### ⚠️ Manejo de Errores y Mensajes
- Se integran los mensajes del framework `django.contrib.messages`.
- Al intentar realizar una acción no permitida, el usuario recibe un mensaje claro mediante `messages.error`.

### 🔄 Migraciones y Base de Datos
- El proyecto incluye las migraciones necesarias para crear las tablas de usuarios, permisos y eventos.
- Se recomienda ejecutar:
```bash
  python manage.py makemigrations
  python manage.py migrate
 ```

### 🚀 Cómo Ejecutar el Proyecto

Clonar el repositorio

git clone https://github.com/OrtegaHamel/M6_AE5_Grupal.git
cd M6_AE5_Grupal


Crear y activar el entorno virtual

```bash
python -m venv venv
source venv/Scripts/activate  # En Windows
```

Aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

Crear superusuario

```bash
python manage.py createsuperuser
```

Ejecutar el servidor

```bash
python manage.py runserver
```

Abrir en el navegador

http://127.0.0.1:8000/


