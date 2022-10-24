from .models import Guests
from django.shortcuts import render
from .forms import AddGuest, AddTable


def wedding_organizer_start_name(request):
    name = request.GET.get('name')
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


def add_new_guest(request):
    if request.method == 'POST':
        # przetwórz odebrane dane i wyswietl
        form_guest = AddGuest(request.POST)
        if form_guest.is_valid():
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            phone = request.POST.get('phone')
            age = request.POST.get('age')
            theSameUserCount = Guests.objects.filter(name = name, surname = surname).count()
            if theSameUserCount != 0:
                return render(request, "add_guest.html", {'guestExist': True, 'guestName': name, 'guestSurname': surname, 'guestPhone': phone, 'guestAge': age})

            form_guest.save()
            return render(request, "add_guest.html", {'afterAdd': True, 'addedGuestName': name})
        else:
            errors = form_guest.errors
            return render(request, "add_guest.html", {'errorGuest': True, 'errorsList': errors})

    else:
        # wyswietl formularz do pobierania danych
        form_guest = AddGuest()
        return render(request, 'add_guest.html', {})


def add_new_table(request):
    if request.method == 'POST':
        form_table = AddTable(request.POST)
        if form_table.is_valid():
            number_of_seats = request.POST.get('number_of_seats')
            table_name = request.POST.get('table_name')
            description = request.POST.get('description')
