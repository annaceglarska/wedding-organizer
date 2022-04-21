

from django import forms
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.generic import View

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


