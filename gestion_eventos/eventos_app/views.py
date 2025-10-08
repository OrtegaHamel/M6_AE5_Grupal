from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import Event, CustomUser

# Home
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
            return Event.objects.filter(attendees=user)

# Crear Evento
class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['title', 'description', 'date', 'is_private']
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)

# Editar Evento
class EventUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Event
    fields = ['title', 'description', 'date', 'is_private']
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('home')
    permission_required = 'events.can_edit_event'

    def has_permission(self):
        event = self.get_object()
        return self.request.user == event.organizer or self.request.user.rol == 'admin'

# Eliminar Evento
class EventDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('home')
    permission_required = 'events.can_delete_event'

    def has_permission(self):
        event = self.get_object()
        return self.request.user == event.organizer or self.request.user.rol == 'admin'

# Detalle de Evento
class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'events/event_detail.html'

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'admin':
            return Event.objects.all()
        elif user.rol == 'organizer':
            return Event.objects.filter(organizer=user)
        else:
            return Event.objects.filter(attendees=user)

# Asistir a Evento
def attend_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user not in event.attendees.all():
        event.attendees.add(request.user)
        messages.success(request, f"Te has registrado al evento {event.title}.")
    else:
        messages.info(request, f"Ya estás registrado en el evento {event.title}.")
    return redirect('event_detail', pk=pk)

