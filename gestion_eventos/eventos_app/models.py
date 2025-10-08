from django.contrib.auth.models import AbstractUser
from django.db import models

# Modelo de Usuario Personalizado
class CustomUser(AbstractUser):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('organizer', 'Organizador'),
        ('attendee', 'Asistente'),
    ]
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default='attendee')

    def __str__(self):
        return self.username

# Modelo de Evento
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    is_private = models.BooleanField(default=False)
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='organized_events')
    attendees = models.ManyToManyField(CustomUser, related_name='attending_events', blank=True)

    class Meta:
        permissions = [
            ('can_edit_event', 'Can edit event'),
            ('can_delete_event', 'Can delete event'),
        ]

    def __str__(self):
        return self.title
