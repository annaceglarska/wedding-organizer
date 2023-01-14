from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.core.serializers import serialize
from .models import Guests, Tables, Seats
from django.views.decorators.csrf import csrf_exempt
import json


def guest_list_endpoint(request):
    guests = Guests.objects.all()
    listGuest = serialize("json", guests)
    return HttpResponse(listGuest, content_type="application/json")


def one_guest_endpoint(request, guest_id):
    guest = Guests.objects.filter(id=guest_id)
    guestJson = serialize("json", guest)
    return HttpResponse(guestJson, content_type="application/json")


@csrf_exempt
def delete(request, table_id):
    if request.method == "DELETE":
        delete_seats(table_id)
        Tables.objects.filter(id=table_id).delete()
        resp = {'status': 'OK'}
        responseJson = json.dumps(resp)
        return HttpResponse(responseJson, content_type="application/json")
    else:
        return HttpResponseBadRequest()


def delete_seats(table_id):
    Seats.objects.filter(table=table_id).delete()  # Ta funkcja ma byc tutaj czy w views?


@csrf_exempt
def delete_guest(request, guest_id):
    if request.method == "DELETE":
        Guests.objects.filter(id=guest_id).delete()
        resp = {'status': 'OK'}
        responseJson = json.dumps(resp)
        return HttpResponse(responseJson, content_type="application/json")
    else:
        return HttpResponseBadRequest()
