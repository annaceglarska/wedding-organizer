from django.forms import ModelForm, ModelChoiceField, Select
from .models import Guests, Tables, Seating


class AddGuest(ModelForm):
    class Meta:
        model = Guests
        fields = ['name', 'surname', 'phone', 'age']


class AddTable(ModelForm):
    class Meta:
        model = Tables
        fields = ['number_of_seats', 'table_name', 'description']


class AddSeating(ModelForm):
    class Meta:
        model = Seating
        fields = ['guest', 'seat']

