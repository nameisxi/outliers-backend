import json

from django.http import HttpResponse

from .src import GithubAPIScraper, GithubObjectCreator


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
