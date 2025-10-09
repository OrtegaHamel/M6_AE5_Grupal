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