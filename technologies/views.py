from urllib import response
from django.http import JsonResponse

from .models import *


def get_unique_technologies(request):
    response = {     
        'programming_languages': list(ProgrammingLanguage.objects.all().order_by('name').distinct('name').values_list('name', flat=True)),
        'technologies': list(Technology.objects.all().order_by('name').distinct('name').values_list('name', flat=True)),
        'topics': list(Topic.objects.all().order_by('name').distinct('name').values_list('name', flat=True)),
    }

    return JsonResponse(response)
