import json

from django.http import HttpResponse

from .src import GithubPopulator


def populate(request):
    populator = GithubPopulator()
    populator.create_github_accounts()
    populator.create_github_repos()
    populator.create_github_programming_languages()
    populator.create_github_metadata()

    return HttpResponse('Done')
