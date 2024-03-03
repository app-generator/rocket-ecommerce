from django.shortcuts import render
from django.core import serializers


# Create your views here.

def index(request):
    context = {
        'segment'  : 'charts',
        'parent'   : 'apps'
    }
    return render(request, 'apps/charts.html', context)
