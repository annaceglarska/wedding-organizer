from .models import Guests, Tables, Seats
from django.shortcuts import render
from .forms import AddGuest, AddTable


def wedding_organizer_start_name(request):
    name = request.GET.get('name')
    return render(request, 'wedding_organizer_start.html', {'name': name})


def guest_list(request):
    guests = Guests.objects.all()
    return render(request, 'guest_list.html', {'guests': guests})


def table_list(request):
    tables = Tables.objects.all()
    return render(request, 'table_list.html', {'tables': tables})


def one_guest(request, guest_id):
    guests = Guests.objects.filter(id=guest_id)
    return render(request, 'guest_list.html', {'guests': guests})


def one_table(request, table_id):
    tables = Tables.objects.filter(id=table_id)
    return render(request, 'table_list.html', {'tables': tables})


def one_guest_with_params(request):
    type = request.GET.get('type')
    value = request.GET.get('value')
    guests = Guests.objects.filter(**{type: value})
    return render(request, 'guest_list.html', {'guests': guests})


def add_new_guest(request):
    if request.method == 'POST':
        form_guest = AddGuest(request.POST)
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        if form_guest.is_valid():

            theSameUserCount = Guests.objects.filter(name=name, surname=surname).count()
            if theSameUserCount != 0:
                return render(request, "add_guest.html",
                              {'guestExist': True, 'guestName': name, 'guestSurname': surname, 'guestPhone': phone,
                               'guestAge': age})

            form_guest.save()
            return render(request, "add_guest.html", {'afterAdd': True, 'addedGuestName': name})
        else:
            errors = form_guest.errors
            return render(request, "add_guest.html", {'errorGuest': True, 'errorsList': errors, 'guestName': name,
                                                      'guestSurname': surname, 'guestPhone': phone, 'guestAge': age})

    else:
        form_guest = AddGuest()
        return render(request, 'add_guest.html', {})


def edit_guest(request, guest_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        phone = request.POST.get('phone')
        age = request.POST.get('age')

        guestToEdit = Guests.objects.get(id=guest_id)
        guestRealName = guestToEdit.name
        guestRealSurname = guestToEdit.surname
        editGuestForm = AddGuest(request.POST, instance=guestToEdit)

        if editGuestForm.is_valid():
            theSameGuestCount = Guests.objects.filter(name=name, surname=surname).count()

            if theSameGuestCount == 0 or (guestRealName == name and guestRealSurname == surname):
                editGuestForm.save()
                return render(request, "edit_guest.html",
                              {'addedGuestName': name, 'addedGuestSurname': surname, 'afterAdd': True})
            else:
                return render(request, "edit_guest.html",
                              {'guestExist': True, 'guestName': name, 'guestSurname': surname, 'guestPhone': phone,
                               'guestAge': age})
        else:
            errors = editGuestForm.errors
            return render(request, "edit_guest.html", {'errorTable': True, 'errorList': errors,
                                                       'guestName': name, 'guestSurname': surname,
                                                       'guestPhone': phone, 'guestAge': age})

    else:
        guestToEdit = Guests.objects.get(id=guest_id)
        return render(request, 'edit_guest.html', {'guestName': guestToEdit.name, 'guestSurname': guestToEdit.surname,
                                                   'guestPhone': guestToEdit.phone, 'guestAge': guestToEdit.age})


def core_new_table(request, table_id):
    isInEditMode = bool(table_id)

    if request.method == 'POST':
        number_of_seats = request.POST.get('number_of_seats')
        table_name = request.POST.get('table_name')
        description = request.POST.get('description')

        if isInEditMode:
            table_to_edit = Tables.objects.get(id=table_id)
            table_real_name = table_to_edit.table_name
            form_table = AddTable(request.POST, instance=table_to_edit)
            old_number_of_seats = Seats.objects.filter(table=table_id).count()
        else:
            form_table = AddTable(request.POST)
            table_real_name = ''

        if form_table.is_valid():

            theSameTableCount = Tables.objects.filter(table_name=table_name).count()

            if theSameTableCount == 0 or table_real_name == table_name:
                form_table.save()
                if isInEditMode:
                    edit_seats(table_id, int(number_of_seats), old_number_of_seats)
                else:
                    just_created_table = Tables.objects.get(table_name=table_name)
                    create_seats(just_created_table.pk, just_created_table.number_of_seats)

                return render(request, "add_table.html",
                              {'afterAdd': True, 'tableName': table_name, 'isInEditMode': isInEditMode})

            else:
                return render(request, "add_table.html", {'tableExist': True, 'tableName': table_name,
                                                          'description': description,
                                                          'numberOfSeats': number_of_seats,
                                                          'isInEditMode': isInEditMode})

        else:
            errors = form_table.errors
            return render(request, 'add_table.html',
                          {'errorTable': True, 'errorList': errors, 'tableName': table_name,
                           'description': description,
                           'numberOfSeats': number_of_seats,
                           'isInEditMode': isInEditMode})
    else:
        if isInEditMode:
            table_to_edit = Tables.objects.get(id=table_id)
            return render(request, 'add_table.html', {'tableName': table_to_edit.table_name,
                                                      'description': table_to_edit.description,
                                                      'numberOfSeats': table_to_edit.number_of_seats,
                                                      'isInEditMode': isInEditMode})
        else:
            return render(request, 'add_table.html', {'isInEditMode': isInEditMode})


def add_new_table(request):
    return core_new_table(request, False)


def edit_new_table(request, table_id):
    return core_new_table(request, table_id)


def create_seats(table_number, current_number_of_seats, old_number_of_seats=0):
    for place_by_table in range(old_number_of_seats + 1, current_number_of_seats + 1):
        seat = Seats(seat_number=place_by_table, table_id=table_number)
        seat.save()


def edit_seats(table_number, current_number_of_seats, old_number_of_seats):
    if old_number_of_seats < current_number_of_seats:
        create_seats(table_number, current_number_of_seats,  old_number_of_seats)
    elif old_number_of_seats > current_number_of_seats:
        for place_by_table in range(old_number_of_seats + 1, current_number_of_seats, -1):
            Seats.objects.filter(seat_number=place_by_table, table=table_number).delete()
