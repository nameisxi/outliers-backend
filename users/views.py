from rest_framework.generics import ListAPIView

from .models import *
from .serializers import *
from .filters import *


class CandidateList(ListAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    filterset_class = CandidateFilter
