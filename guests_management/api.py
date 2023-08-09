from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.core.serializers import serialize
from .models import Guests, Tables, Seating, Seats
from django.views.decorators.csrf import csrf_exempt
import json
from .helpers import free_seat_for_table, get_seats_with_seating_by_one_table


def guest_list_endpoint(request):
    guests = Guests.objects.all()
    listGuest = serialize("json", guests)
    return HttpResponse(listGuest, content_type="application/json")


def one_guest_endpoint(request, guest_id):
    guest = Guests.objects.filter(id=guest_id)
    guestJson = serialize("json", guest)
    return HttpResponse(guestJson, content_type="application/json")


@csrf_exempt
def get_free_seats_in_table(request, table_id):
    free_seats = free_seat_for_table(table_id)
    response_Json = json.dumps(free_seats)
    return HttpResponse(response_Json, content_type="application/json")


@csrf_exempt
def delete_seating(request, seat_id):
    if request.method == "DELETE":
        Seating.objects.filter(seat_id=seat_id).delete()
        resp = {'status': 'OK'}
        responseJson = json.dumps(resp)
        return HttpResponse(responseJson, content_type="application/json")
    else:
        return HttpResponseBadRequest()


@csrf_exempt
def delete(request, table_id):
    if request.method == "DELETE":
        Tables.objects.filter(id=table_id).delete()
        resp = {'status': 'OK'}
        responseJson = json.dumps(resp)
        return HttpResponse(responseJson, content_type="application/json")
    else:
        return HttpResponseBadRequest()


@csrf_exempt
def delete_guest(request, guest_id):
    if request.method == "DELETE":
        Guests.objects.filter(id=guest_id).delete()
        resp = {'status': 'OK'}
        responseJson = json.dumps(resp)
        return HttpResponse(responseJson, content_type="application/json")
    else:
        return HttpResponseBadRequest()


@csrf_exempt
def seating_by_one_table(request, table_id):
    taken_seats = get_seats_with_seating_by_one_table(table_id)
    response_json = json.dumps(taken_seats)
    return HttpResponse(response_json, content_type="application/json")






