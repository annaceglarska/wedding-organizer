from django.forms import ModelForm
from .models import Guests, Tables


class AddGuest(ModelForm):
    class Meta:
        model = Guests
        fields = ['name', 'surname', 'phone', 'age']


class AddTable(ModelForm):
    class Meta:
        model = Tables
        fields = ['number_of_seats', 'table_name', 'description']

