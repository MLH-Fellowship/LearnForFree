import json

from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers
from django.core.paginator import Paginator

from django.shortcuts import render

from .models import course
from .models import content_provider

def index(request):
    return render(request, 'templates/index.html', {
        'error_message': "Error.!",
    })

def results(request):
    request_value = request.GET.get('keywords', "")
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)

    # with open('content_provider_config.json') as f:
    #    data = json.load(f)

    #provider_data = {
    #   "name": "Futurelearn",
    #   "web_search_url": "https://www.futurelearn.com/search?q="
    #}

    #provider_data = {
    #    "name": "edX",
    #    "web_search_url": "https://www.edx.org/"
    #}

    with open("content_provider_config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    results = []

    for prov_name, prov_data in config.items():
        print(prov_data)
        provider = content_provider.ContentProvider(prov_data)
        resultlist = provider.provide(request_value);
        for result in resultlist:
            result = result.as_dict()
            results.append(result)

    #paginate
    paginator = Paginator(results, page_size)
    page_obj = paginator.get_page(page_number)

    # add keywords back to data to use on the frontend
    page_obj.keywords = request_value


    #return JsonResponse(results, safe=False)
    return render(request, 'templates/index.html', {"results": page_obj})
