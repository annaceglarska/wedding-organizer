from dataclasses import dataclass

from .enums import StatusEnum, ErrorsEnum
from .models import Guests, Tables, Seats
from django.shortcuts import render, redirect
from .forms import AddGuest, AddTable, Seating, AddSeating
from .helpers import tables_able_to_assign_guest, \
    find_seat_assign_to_the_guest, find_table_name_assign_to_the_guest, \
    get_seats_with_seating_by_one_table, get_guest_with_seating, edit_seats, create_seats
from .views import render_seating_view, add_edit_guest, add_edit_table


def wedding_organizer_start_name(request):
    name = request.GET.get('name')
    return render(request, 'wedding_organizer_start.html', {'name': name})


def guest_list(request):
    guests_with_seating = get_guest_with_seating()

    return render(request, 'guest_list.html', {'guests': guests_with_seating})


def table_list(request):
    tables = Tables.objects.all()
    for table in tables:
        table.seat_with_seating = get_seats_with_seating_by_one_table(table_id=table.id,
                                                                      with_empty_seats=True)
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


@dataclass
class ErrorInformation:
    error_type = None
    error_list = None


def add_new_guest(request):
    @dataclass
    class GuestObject:
        name: str = request.POST.get('name')
        surname: str = request.POST.get('surname')
        phone: str = request.POST.get('phone')
        age: str = request.POST.get('age')

    if request.method == 'POST':
        form_guest = AddGuest(request.POST)
        guest = GuestObject()
        error_information = ErrorInformation()

        if form_guest.is_valid():

            the_same_user_count = Guests.objects.filter(name=guest.name, surname=guest.surname).count()
            if the_same_user_count != 0:
                error_information.error_type = ErrorsEnum.GUEST_EXIST
                return add_edit_guest(request, status_type=StatusEnum.ERROR, guest_object=guest,
                                      error_information=error_information)

            form_guest.save()
            return add_edit_guest(request, status_type=StatusEnum.OK, guest_object=guest)

        else:
            error_information.error_list = form_guest.errors
            error_information.error_type = ErrorsEnum.GUEST_ERROR
            return add_edit_guest(request, status_type=StatusEnum.ERROR, error_information=error_information, guest_object=guest)

    else:
        return add_edit_guest(request, status_type=StatusEnum.BEFORE_ADD)


def edit_guest(request, guest_id):
    if request.method == 'POST':
        @dataclass
        class GuestObject:
            name: str = request.POST.get('name')
            surname: str = request.POST.get('surname')
            phone: str = request.POST.get('phone')
            age: str = request.POST.get('age')

        guest = GuestObject()
        error_information = ErrorInformation()

        guest_to_edit = Guests.objects.get(id=guest_id)
        guest_real_name = guest_to_edit.name
        guest_real_surname = guest_to_edit.surname
        edit_guest_form = AddGuest(request.POST, instance=guest_to_edit)

        if edit_guest_form.is_valid():
            theSameGuestCount = Guests.objects.filter(name=guest.name, surname=guest.surname).count()

            if theSameGuestCount == 0 or (guest_real_name == guest.name and guest_real_surname == guest.surname):
                edit_guest_form.save()
                return add_edit_guest(request, status_type=StatusEnum.OK, edition=True, guest_object=guest)

            else:
                error_information.error_type = ErrorsEnum.GUEST_EXIST
                return add_edit_guest(request, status_type=StatusEnum.ERROR, edition=True, guest_object=guest,
                                      error_information=error_information)

        else:
            error_information.error_list = edit_guest_form.errors
            error_information.error_type = ErrorsEnum.GUEST_ERROR
            return add_edit_guest(request, status_type=StatusEnum.ERROR, edition=True, guest_object=guest,
                                  error_information=error_information)

    else:
        guest_to_edit = Guests.objects.get(id=guest_id)
        return add_edit_guest(request, status_type=StatusEnum.BEFORE_ADD, edition=True, guest_object=guest_to_edit)


def core_new_table(request, table_id):

    @dataclass
    class TableObject:
        number_of_seats: str = request.POST.get('number_of_seats')
        table_name: str = request.POST.get('table_name')
        description: str = request.POST.get('description')

    table = TableObject()
    error_information = ErrorInformation()

    is_in_edit_mode = bool(table_id)

    if request.method == 'POST':

        if is_in_edit_mode:
            table_to_edit = Tables.objects.get(id=table_id)
            table_real_name = table_to_edit.table_name
            form_table = AddTable(request.POST, instance=table_to_edit)
            old_number_of_seats = Seats.objects.filter(table=table_id).count()
        else:
            form_table = AddTable(request.POST)
            table_real_name = ''

        if form_table.is_valid():

            the_same_table_count = Tables.objects.filter(table_name=table.table_name).count()

            if the_same_table_count == 0 or table_real_name == table.table_name:
                form_table.save()
                if is_in_edit_mode:
                    edit_seats(table_id, int(table.number_of_seats), old_number_of_seats)
                else:
                    just_created_table = Tables.objects.get(table_name=table.table_name)
                    create_seats(just_created_table.pk, just_created_table.number_of_seats)

                return add_edit_table(request, status_type=StatusEnum.OK, table_object=table,
                                      edition_information={'table_to_edit_id': is_in_edit_mode})

            else:
                error_information.error_type = ErrorsEnum.TABLE_EXIST
                return add_edit_table(request, status_type=StatusEnum.ERROR, table_object=table,
                                      edition_information={'table_to_edit_id': is_in_edit_mode},
                                      error_information=error_information)
        else:
            error_information.error_list = form_table.errors
            error_information.error_type = ErrorsEnum.TABLE_ERROR
            return add_edit_table(request, status_type=StatusEnum.ERROR, table_object=table,
                                  edition_information={'table_to_edit_id': is_in_edit_mode},
                                  error_information=error_information)
    else:
        if is_in_edit_mode:
            table_to_edit = Tables.objects.get(id=table_id)
            return add_edit_table(request, status_type=StatusEnum.BEFORE_ADD, table_object=table_to_edit,
                                  edition_information={'table_to_edit_id': is_in_edit_mode})
        else:
            return add_edit_table(request, status_type=StatusEnum.BEFORE_ADD, table_object=table,
                                  edition_information={'table_to_edit_id': is_in_edit_mode})


def add_new_table(request):
    return core_new_table(request, False)


def edit_new_table(request, table_id):
    return core_new_table(request, table_id)


def create_seating(request):
    @dataclass
    class SeatingObject:
        guest = request.POST.get('guest')
        seat_number = request.POST.get('seat')

    if request.method == 'POST':
        seating = SeatingObject()
        error_information = ErrorInformation()

        seating_form = AddSeating(request.POST)
        if seating_form.is_valid():
            the_same_guest_in_seating_count = Seating.objects.filter(guest_id=seating.guest).count()
            the_same_seat_in_seating_count = Seating.objects.filter(seat_id=seating.seat_number).count()
            if the_same_guest_in_seating_count != 0 and the_same_seat_in_seating_count != 0:
                error_information.error_type = ErrorsEnum.SEATING_EXIST
                return render_seating_view(request=request, status_type=StatusEnum.BEFORE_ADD,
                                           error_information=error_information)

            seating_form.save()
            guest = int(seating.guest)
            guest_object = Guests.objects.get(id=guest)
            return render_seating_view(request=request, status_type=StatusEnum.OK,
                                       guest_object=guest_object)

        else:
            error_information.error_list = seating_form.errors
            error_information.error_type = ErrorsEnum.GUEST_ERROR
            return render_seating_view(request=request, status_type=StatusEnum.ERROR,
                                       error_information=error_information)
    else:
        return render_seating_view(request=request, status_type=StatusEnum.BEFORE_ADD)


def edit_seating(request, seating_id):
    @dataclass
    class EditionInformation:
        guest_to_edit_id = None
        table_name = None
        seat_number = None

    edition_information = EditionInformation()

    seating = Seating.objects.get(id=seating_id)
    seat = find_seat_assign_to_the_guest(seating)
    edition_information.seat_number = seat.number
    edition_information.table_name = find_table_name_assign_to_the_guest(seat)
    edition_information.guest_id = seating.guest_id

    error_information = ErrorInformation()

    if request.method == 'POST':
        seating_to_edit = Seating.objects.get(id=seating_id)
        edit_seating_form = AddSeating(request.POST, instance=seating_to_edit)

        if edit_seating_form.is_valid():
            edit_seating_form.save()
            return render_seating_view(request=request, status_type=StatusEnum.OK,
                                       edition_information=edition_information)
        else:
            error_information.error_list = edit_seating_form.errors
            error_information.error_type = ErrorsEnum.SEATING_ERROR
            return render_seating_view(request=request, status_type=StatusEnum.ERROR,
                                       error_information=error_information,
                                       edition_information=edition_information)

    else:
        return render_seating_view(request=request, status_type=StatusEnum.BEFORE_ADD,
                                   edition_information=edition_information)


def delete_seating(request, seating_id):
    Seating.objects.filter(id=seating_id).delete()
    return redirect(guest_list)
