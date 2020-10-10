import json

from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers

from django.shortcuts import render

from .models import course


def index(request):
    return render(request, 'templates/index.html', {
        'error_message': "Error.!",
    })

def results(request, keywords):
    result1 = course.Course('Course name 1', 'Lorem ipsum description 1', 'Coursera',
                            'https://www.coursera.org/',
                            'https://storage-prtl-co.imgix.net/endor/organisations/17569/logos/1511918356_Coursera.png')
    result2 = course.Course('Course name 2', 'Lorem ipsum description 2', 'edX',
                            'https://www.edx.org/',
                            'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTWOwoKSJqRKu-9-FD_-nsVhJWOSiGAIPHTRQ&usqp=CAU')
    resultlist = [result1.as_dict(), result2.as_dict()]
    print(resultlist)

    return JsonResponse(resultlist, safe=False)
