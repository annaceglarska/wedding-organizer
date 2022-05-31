from .models import Guests
from django.shortcuts import render


def wedding_organizer_start_name(request, name=''):
    return render(request, 'wedding_organizer_start.html', {'name': name})


def guest_list(request):
    guests = Guests.objects.all()
    return render(request, 'guest_list.html', {'guests': guests})


def one_guest(request, guest_id):
    guests = Guests.objects.filter(id=guest_id)
    return render(request, 'guest_list.html', {'guests': guests})


def one_guest_with_params(request):
    type = request.GET.get('type')
    value = request.GET.get('value')
    guests = Guests.objects.filter(**{type: value})
    return render(request, 'guest_list.html', {'guests': guests})
