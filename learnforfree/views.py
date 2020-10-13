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

def results(request):
    request_value = request.GET.get('keywords')

    # with open('content_provider_config.json') as f:
    #    data = json.load(f)

    provider_data = {
       "name": "futurelearn",
       "web_search_url": "https://www.futurelearn.com/search?q="
    }

    # provider_data = {
    #     "name": "edx",
    #     "web_search_url": "https://www.edx.org/"
    # }

    provider = content_provider.ContentProvider(provider_data)
    resultlist = provider.provide(request_value);
    results = []
    for result in resultlist:
        result = result.as_dict()
        results.append(result)

    # print(resultlist)

    #return JsonResponse(results, safe=False)
    return render(request, 'templates/index.html', {"results": results})
