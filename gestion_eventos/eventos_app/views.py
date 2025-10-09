from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import Event, CustomUser

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_invalid(self, form):
        messages.error(
            self.request,
            "❌ ¡ATENCIÓN! Usuario o contraseña incorrectos. "
            "Por favor, verifica tus credenciales e inténtalo de nuevo. "
            "Si olvidaste tu contraseña, contacta al administrador del sistema."
        )
        return super().form_invalid(form)

class HomeView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/home.html'
    context_object_name = 'events'

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'admin':
            return Event.objects.all()
        elif user.rol == 'organizer':
            return Event.objects.filter(organizer=user)
        else:
            return Event.objects.filter(is_private=False) | Event.objects.filter(attendees=user)

class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

class EventCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Event
    fields = ['title', 'description', 'date', 'is_private']
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.rol in ['admin', 'organizer']

    def handle_no_permission(self):
        messages.error(self.request, "¡ACCESO DENEGADO! No tienes los permisos necesarios para crear eventos.")
        return redirect('home')

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    fields = ['title', 'description', 'date', 'is_private']
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        event = self.get_object()
        return self.request.user.rol == 'admin' or self.request.user == event.organizer

    def handle_no_permission(self):
        messages.error(self.request, "¡ACCESO DENEGADO! No puedes editar este evento.")
        return redirect('home')

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.rol == 'admin'

    def handle_no_permission(self):
        messages.error(self.request, "¡ACCESO DENEGADO! No tienes permiso para eliminar este evento.")
        return redirect('home')

def attend_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user not in event.attendees.all():
        event.attendees.add(request.user)
        messages.success(request, f"Te has registrado al evento {event.title}.")
    else:
        messages.info(request, f"Ya estás registrado en el evento {event.title}.")
    return redirect('event_detail', pk=pk)


