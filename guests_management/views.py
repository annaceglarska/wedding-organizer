from django.shortcuts import render
from .enums import StatusEnum, ErrorsEnum
from guests_management.helpers import guest_not_assign_to_seat, tables_able_to_assign_guest
from .models import Guests


default_edition_information = {
    'guest_to_edit_id': None,
    'table_name': None,
    'seat_number': None
}

default_table_edition_information = {
    'table_to_edit_id': False
}


def render_seating_view(request, status_type, guest_object=None,
                        error_information=None,
                        edition_information=None):
    free_guests = guest_not_assign_to_seat()
    free_tables = tables_able_to_assign_guest()

    if getattr(edition_information, 'guest_to_edit_id', None):
        guest_id = getattr(edition_information, 'guest_to_edit_id', None)
        guest = Guests.objects.get(id=guest_id)
        guest_to_render = [guest]

    guest_to_edit_id = getattr(edition_information, 'guest_to_edit_id', None)

    return render(request, 'seating_form.html',
                  {
                      'guests': guest_to_render if guest_to_edit_id else free_guests,
                      'tables': free_tables, 'status_type': status_type,
                      'error_type': error_information.error_type if error_information else None,
                      'guest': guest if guest_to_edit_id else guest_object,
                      'error_list': error_information.error_list if error_information else None,
                      'ErrorsEnum': ErrorsEnum, 'StatusEnum': StatusEnum,
                      'edition':  bool(guest_to_edit_id),
                      'table_name': edition_information.table_name if edition_information else None,
                      'seat_number': edition_information.seat_number if edition_information else None})


def add_edit_guest(request, status_type, edition=False, guest_object=None,
                   error_information=None):
    html_file_name = "edit_guest.html" if edition else "add_guest.html"

    return render(request, html_file_name, {'guestName': guest_object.name if guest_object else None,
                                            'guestSurname': guest_object.surname if guest_object else None,
                                            'guestPhone': guest_object.phone if guest_object else None,
                                            'guestAge': guest_object.age if guest_object else None,
                                            'ErrorsEnum': ErrorsEnum, 'StatusEnum': StatusEnum,
                                            'status_type': status_type,
                                            'errorList': error_information.error_list if error_information else None,
                                            'error_type': error_information.error_type if error_information else None})


def add_edit_table(request, status_type, table_object=None, edition_information=default_table_edition_information,
                   error_information=None):
    return render(request, "add_table.html", {'status_type': status_type,
                                              'tableName': table_object.table_name,
                                              'description': table_object.description,
                                              'numberOfSeats': table_object.number_of_seats,
                                              'isInEditMode': edition_information['table_to_edit_id'],
                                              'error_type': error_information.error_type if error_information else None,
                                              'errorList': error_information.error_list if error_information else None,
                                              'ErrorsEnum': ErrorsEnum, 'StatusEnum': StatusEnum})
