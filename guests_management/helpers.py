from django.forms import model_to_dict

from .models import Guests, Seating, Tables, Seats


def guest_not_assign_to_seat():
    guests = []
    guests_data = Guests.objects.all()
    for guest_data in guests_data:
        isFoundSeating = Seating.objects.filter(guest_id=guest_data.id).exists()
        if not isFoundSeating:
            guest = Guests.objects.get(id=guest_data.id)
            guests.append(guest)

    return guests


def get_guest_with_seating():
    guests = Guests.objects.all()
    for one_guest in guests:
        guest_seating = Seating.objects.filter(guest_id=one_guest.id).first()
        if guest_seating:
            seat = find_seat_assign_to_the_guest(guest_seating)
            one_guest.seat_number = seat.seat_number
            one_guest.table_name = find_table_name_assign_to_the_guest(seat)
            one_guest.seating_id = guest_seating.id

    return guests


def tables_able_to_assign_guest():
    tables = []
    all_tables = Tables.objects.all()
    for table in all_tables:
        free_seats = free_seat_for_table(table.id)
        if free_seats:
            table = Tables.objects.get(id=table.id)
            tables.append(table)

    return tables


def free_seat_for_table(table_id):
    all_seats_in_table = Seats.objects.filter(table_id=table_id)
    free_seats = []
    for seat in all_seats_in_table:
        isSeatOccupied = Seating.objects.filter(seat_id=seat.id).exists()
        if not isSeatOccupied:
            seat = Seats.objects.get(id=seat.id)
            seat_info = {
                'seatId': seat.id,
                'seatNumber': seat.seat_number
            }
            free_seats.append(seat_info)

    return free_seats


def find_seat_assign_to_the_guest(guest_seating):
    seat_id = guest_seating.seat_id
    seat = Seats.objects.get(id=seat_id)
    return seat


def find_table_name_assign_to_the_guest(seat):
    table_id = seat.table_id
    table = Tables.objects.get(id=table_id)
    table_name = table.table_name
    return table_name


def get_seats_with_seating_by_one_table(table_id, with_empty_seats=False):
    seats_by_table = Seats.objects.filter(table_id=table_id)
    responseArray = []
    for seat in seats_by_table:
        seating = Seating.objects.filter(seat_id=seat.id).first()
        seat_dict = {
                'id': seat.id,
                'seat_number': seat.seat_number,
                'table_id': table_id,
            }
        if seating:
            guest_id = seating.guest_id
            guest = Guests.objects.get(id=guest_id)
            seat_dict['seating_id'] = seating.id
            seat_dict['guest'] = {
                "name": guest.name,
                "surname": guest.surname
            }
            responseArray.append(seat_dict)

        if with_empty_seats and not seating:
            responseArray.append(seat_dict)

    return responseArray


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



