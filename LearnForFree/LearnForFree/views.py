import json

from django.http import JsonResponse
from django.core import serializers

from django.shortcuts import render

from .models import course


def index(request):
    return render(request, 'templates/index.html', {
        'error_message': "Error.!",
    })

def results(request, keywords):
    result1 = course.Course('Course name 1', 'Lorem ipsum description 1')
    result2 = course.Course('Course name 2', 'Lorem ipsum description 2')
    resultlist = [result1.toJSON(), result2.toJSON()]

    return JsonResponse({'results': resultlist})