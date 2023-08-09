from django.shortcuts import render
from .enums import StatusEnum, ErrorsEnum
from guests_management.helpers import guest_not_assign_to_seat, tables_able_to_assign_guest
from .models import Guests

default_error_information = {
    'error_type': None,
    'error_list': None
}

default_edition_information = {
    'guest_to_edit_id': None,
    'table_name': None,
    'seat_number': None
}


def render_seating_view(request, status_type, guest_object=None,
                        error_information=default_error_information,
                        edition_information=default_edition_information):
    free_guests = guest_not_assign_to_seat()
    free_tables = tables_able_to_assign_guest()

    if edition_information['guest_to_edit_id']:
        guest = Guests.objects.get(id=edition_information['guest_to_edit_id'])
        guest_to_render = [guest]

    return render(request, 'seating_form.html',
                  {
                      'guests': guest_to_render if edition_information['guest_to_edit_id'] else free_guests,
                      'tables': free_tables, 'status_type': status_type,
                      'error_type': error_information['error_type'],
                      'guest': guest if edition_information['guest_to_edit_id'] else guest_object,
                      'error_list': error_information['error_list'],
                      'ErrorsEnum': ErrorsEnum, 'StatusEnum': StatusEnum,
                      'edition': edition_information['guest_to_edit_id'] is not None,
                      'table_name': edition_information['table_name'],
                      'seat_number': edition_information['seat_number']})
