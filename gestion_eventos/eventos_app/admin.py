from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Event

# Personalizar el admin para CustomUser
class CustomUserAdmin(UserAdmin):
    # Campos a mostrar en la lista de usuarios
    list_display = ('username', 'email', 'rol', 'is_staff')
    # Campos para filtrar
    list_filter = ('rol', 'is_staff', 'is_superuser')
    # Campos a mostrar en el formulario de edición
    fieldsets = UserAdmin.fieldsets + (
        ('Rol', {'fields': ('rol',)}),
    )
    # Campos a mostrar al agregar un nuevo usuario
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rol', {'fields': ('rol',)}),
    )

# Registrar CustomUser con el admin personalizado
admin.site.register(CustomUser, CustomUserAdmin)

# Registrar Event
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'organizer', 'is_private')
    list_filter = ('is_private', 'date')
    search_fields = ('title', 'description')
    filter_horizontal = ('attendees',)

