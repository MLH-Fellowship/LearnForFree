import json

from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers

from django.shortcuts import render

from .models import course
from .models import content_provider

def index(request):
    return render(request, 'templates/index.html', {
        'error_message': "Error.!",
    })

def results(request, keywords):
    # with open('content_provider_config.json') as f:
    #    data = json.load(f)

    provider_data = {
        "name": "edx",
        "web_search_url": "https://www.edx.org/search?q="
    }

    provider = content_provider.ContentProvider(provider_data)
    resultlist = provider.provide(keywords);
    for result in resultlist:
        result = result.as_dict()

    print(resultlist)

    return JsonResponse(resultlist, safe=False)
