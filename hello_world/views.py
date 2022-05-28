
from .models import Guests
import mpmath
from django.shortcuts import render


def hello_world_name(request, name=''):
    return render(request, 'hello_world.html', {'name': name})

def calculate(request, value):
    first = value
    sec = mpmath.rand()
    ans = first * sec
    return render(request, 'calculation.html', {'first': first, 'sec': sec, 'ans': ans})


def guestList(request):
    guests = Guests.objects.all()
    return render(request, 'guest_list.html', {'guests': guests})


def oneGuest(request, guest_id):
    guests = Guests.objects.filter(id=guest_id)
    return render(request, 'guest_list.html', {'guests': guests})


def oneGuestWithParams(request):
    #  getOneGuestByParams
    type = request.GET.get('type')
    value = request.GET.get('value')
    guests = Guests.objects.filter(**{type:value})
    return render(request, 'guest_list.html', {'guests': guests})
