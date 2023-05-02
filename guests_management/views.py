from .models import Guests, Tables, Seats
from django.shortcuts import render, redirect
from .forms import AddGuest, AddTable, Seating, AddSeating
from .helpers import guest_not_assign_to_seat, tables_able_to_assign_guest, \
    find_seat_assign_to_the_guest, find_table_name_assign_to_the_guest


def wedding_organizer_start_name(request):
    name = request.GET.get('name')
    return render(request, 'wedding_organizer_start.html', {'name': name})


def guest_list(request):
    guests = Guests.objects.all()
    for one_guest in guests:
        guest_seating = Seating.objects.filter(guest_id=one_guest.id).first()
        if guest_seating:
            seat = find_seat_assign_to_the_guest(guest_seating)
            one_guest.seat_number = seat.seat_number
            one_guest.table_name = find_table_name_assign_to_the_guest(seat)
            one_guest.seating_id = guest_seating.id

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
                              {'guestExist': True, 'guestName': name, 'guestSurname': surname,
                               'guestPhone': phone,
                               'guestAge': age})

            form_guest.save()
            return render(request, "add_guest.html", {'afterAdd': True, 'addedGuestName': name})
        else:
            errors = form_guest.errors
            return render(request, "add_guest.html",
                          {'errorGuest': True, 'errorsList': errors, 'guestName': name,
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
                              {'addedGuestName': name, 'addedGuestSurname': surname,
                               'afterAdd': True})
            else:
                return render(request, "edit_guest.html",
                              {'guestExist': True, 'guestName': name, 'guestSurname': surname,
                               'guestPhone': phone,
                               'guestAge': age})
        else:
            errors = editGuestForm.errors
            return render(request, "edit_guest.html", {'errorTable': True, 'errorList': errors,
                                                       'guestName': name, 'guestSurname': surname,
                                                       'guestPhone': phone, 'guestAge': age})

    else:
        guestToEdit = Guests.objects.get(id=guest_id)
        return render(request, 'edit_guest.html',
                      {'guestName': guestToEdit.name, 'guestSurname': guestToEdit.surname,
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
                              {'afterAdd': True, 'tableName': table_name,
                               'isInEditMode': isInEditMode})

            else:
                return render(request, "add_table.html",
                              {'tableExist': True, 'tableName': table_name,
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
        create_seats(table_number, current_number_of_seats, old_number_of_seats)
    elif old_number_of_seats > current_number_of_seats:
        for place_by_table in range(old_number_of_seats + 1, current_number_of_seats, -1):
            Seats.objects.filter(seat_number=place_by_table, table=table_number).delete()


def create_seating(request):
    free_guests = guest_not_assign_to_seat()
    free_tables = tables_able_to_assign_guest()

    if request.method == 'POST':
        seating_form = AddSeating(request.POST)
        guest = request.POST.get('guest')
        seat_number = request.POST.get('seat')

        if seating_form.is_valid():

            the_same_guest_in_seating_count = Seating.objects.filter(guest_id=guest).count()
            the_same_seat_in_seating_count = Seating.objects.filter(seat_id=seat_number).count()
            if the_same_guest_in_seating_count != 0 and the_same_seat_in_seating_count != 0:
                return render(request, 'seating_form.html', {'seating_exist': True,
                                                             'guests': free_guests,
                                                             'tables': free_tables})

            seating_form.save()
            guest = int(guest)
            guest_object = Guests.objects.get(id=guest)
            return render(request, 'seating_form.html', {'after_add': True,
                                                         'seated_guest': guest_object,
                                                         'guests': free_guests,
                                                         'tables': free_tables})
        else:
            errors = seating_form.errors
            return render(request, 'seating_form.html', {'errorGuest': True, 'error_list': errors,
                                                         'guests': free_guests,
                                                         'tables': free_tables})
    else:
        seating_form = AddSeating()
        return render(request, 'seating_form.html', {'guests': free_guests, 'tables': free_tables})


def edit_seating(request, seating_id):
    free_tables = tables_able_to_assign_guest()

    seating = Seating.objects.get(id=seating_id)
    seat = find_seat_assign_to_the_guest(seating)
    table_name = find_table_name_assign_to_the_guest(seat)
    guest_id = seating.guest_id
    guest = Guests.objects.get(id=guest_id)
    guest_to_render = [guest]

    if request.method == 'POST':
        guest = request.POST.get('guest')
        table = request.POST.get('table')
        seat_number = request.POST.get('seat')

        seating_to_edit = Seating.objects.get(id=seating_id)
        edit_seating_form = AddSeating(request.POST, instance=seating_to_edit)

        if edit_seating_form.is_valid():
            edit_seating_form.save()
            return render(request, 'seating_form.html',
                          {'edition': True, 'after_add': True, 'guests': guest_to_render,
                           'guest': guest, 'table_name': table_name, 'seat_number': seat.seat_number})
        else:
            errors = edit_seating_form.errors
            return render(request, 'seating_form.html', {'edition': True, 'error_seating': True,
                                                         'error_list': errors,
                                                         'guests': guest_to_render,
                                                         'tables': free_tables,
                                                         'guest': guest, 'table_name': table_name,
                                                         'seat_number': seat.seat_number
                                                         })
    else:
        return render(request, 'seating_form.html', {'edition': True, 'guests': guest_to_render,
                                                     'tables': free_tables,
                                                     'table_name': table_name,
                                                     'seat_number': seat.seat_number,
                                                     'guest': guest})


def delete_seating(request, seating_id):
    Seating.objects.filter(id=seating_id).delete()
    return redirect(guest_list)

