from django.forms import ModelForm
from .models import Guests


class AddGuest(ModelForm):
    class Meta:
        model = Guests
        fields = ['name', 'surname', 'phone', 'age']