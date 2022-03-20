import math

import mpmath
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.shortcuts import render


def hello_world(request, name):
    return render(request, 'hello_world.html', {'name' : name})

def calculate(request, value):
    first = value
    sec = mpmath.rand()
    ans = first * sec
    return render(request, 'calculation.html', {'first': first, 'sec': sec, 'ans': ans})

