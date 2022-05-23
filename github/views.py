import json

from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .src import GithubAPIScraper, GithubObjectCreator
from .models import *
from .serializers import *


def scrape(request):
    """
    Executes a pipeline that populates the database with Github data that has been gathered using the Github REST API.
    """
    scraper = GithubAPIScraper()
    scraper.scrape()

    return HttpResponse('Done')

def populate(request):
    """
    Executes a pipeline that populates the database with Github data that has been gathered using the Github REST API.
    """
    creator = GithubObjectCreator()
    creator.create()
    # populator.create_github_accounts()
    # populator.create_github_repos()
    # populator.create_github_programming_languages()
    # populator.create_github_metadata()

    return HttpResponse('Done')


class GithubAccountView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, candidate_id):
        github_account = GithubAccount.objects.get(owner__id=candidate_id)
        serializer = FullGithubAccountSerializer(github_account, many=False)

        return Response(serializer.data)
