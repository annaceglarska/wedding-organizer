import requests
from django import forms
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.core.serializers import serialize
from .models import Guests


class AddTwoNumbersForm(forms.Form):
    first = forms.DecimalField()
    second = forms.DecimalField()


def addTwoNumbersView(request):
    form = AddTwoNumbersForm(request.GET)
    if form.is_valid():
        params = form.cleaned_data
        result = params['first'] + params['second']
        return JsonResponse({'result': result})
    return HttpResponseBadRequest()


def guest_list_endpoint(request):
    guests = Guests.objects.all()
    listGuest = serialize("json", guests)
    return HttpResponse(listGuest, content_type="application/json")


def one_guest_endpoint(request, guest_id):
    guest = Guests.objects.filter(id=guest_id)
    guestJson = serialize("json", guest)
    return HttpResponse(guestJson, content_type="application/json")


