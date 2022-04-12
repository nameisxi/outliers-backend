from django.http.response import JsonResponse
from rest_framework.generics import GenericAPIView

from users.models import Candidate


class LeadView(GenericAPIView):
    """
    API endpoint to get a lead, e.g. a Candidate model object.
    """
    # queryset = ''
    # serializer_class = LeadSerializer
    # pagination_class = None

    #@method_decorator(cache_page(CACHE_TTL))
    def get(self, request, lead_id=None, parameters=None):
        
        return JsonResponse({})

class LeadSetView(GenericAPIView):
    """
    API endpoint to get a lead set, e.g. a set of Candidate model objects connected to a job opening.
    """
    # queryset = ''
    # serializer_class = LeadSerializer
    # pagination_class = None

    #@method_decorator(cache_page(CACHE_TTL))
    def get(self, request, lead_set_id=None, parameters=None):
        
        return JsonResponse({})
