import os
from datetime import timedelta

from django.http import HttpResponse
from django.db.models import Count
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny

from .src import GithubAPIScraper, GithubObjectCreator
from .models import *
from .serializers import *


def scrape(request):
    """
    Executes a scraping pipeline that scrapes Github via the Github REST API.
    """
    scraper = GithubAPIScraper()
    creator = GithubObjectCreator()

    # scraper.scrape()

    # scraper.scrape_accounts()
    creator.create_github_accounts()
    creator.create_github_repos()
    creator.create_github_programming_languages()
    creator.create_github_organizations()
    creator.create_github_contributions_calendars()

    scraper.scrape_repos()
    creator.create_github_repos()

    scraper.scrape_languages()
    creator.create_github_programming_languages()

    scraper.scrape_organizations()
    creator.create_github_organizations()

    scraper.scrape_contributions()
    creator.create_github_contributions_calendars()

    creator.create_github_metadata()

    return HttpResponse('Done')

def scrape_accounts(request):
    """
    Executes a scraping pipeline that scrapes Github accounts via the Github REST API.
    """
    scraper = GithubAPIScraper()
    scraper.scrape_accounts()

    # TODO: update to GraphQL implementation

    return HttpResponse('Done')

def scrape_repos(request):
    """
    Executes a scraping pipeline that scrapes Github repos via the Github REST API.
    """
    scraper = GithubAPIScraper()
    scraper.scrape_repos()

    creator = GithubObjectCreator()
    creator.create_github_repos()

    return HttpResponse('Done')

def scrape_organizations(request):
    """
    Executes a scraping pipeline that scrapes Github organizations via the Github REST API.
    """
    scraper = GithubAPIScraper()
    scraper.scrape_organizations()

    creator = GithubObjectCreator()
    creator.create_github_organizations()

    return HttpResponse('Done')

def scrape_contributions(request):
    """
    Executes a scraping pipeline that scrapes Github contributions via the Github REST API.
    """
    scraper = GithubAPIScraper()
    scraper.scrape_contributions()

    creator = GithubObjectCreator()
    creator.create_github_contributions_calendars()

    return HttpResponse('Done')

def scrape_languages(request):
    """
    Executes a scraping pipeline that scrapes Github languages via the Github REST API.
    """
    scraper = GithubAPIScraper()
    scraper.scrape_languages()

    creator = GithubObjectCreator()
    creator.create_github_programming_languages()

    return HttpResponse('Done')

def populate(request):
    """
    Executes a pipeline that populates the database with Github data that has been gathered using the Github REST API.
    """
    creator = GithubObjectCreator()
    creator.create()

    return HttpResponse('Done')

def populate_accounts(request):
    """
    Executes a pipeline that populates the database with Github account data that has been gathered using the Github REST API.
    """
    creator = GithubObjectCreator()
    creator.create_github_accounts()

    return HttpResponse('Done')

def populate_metadata(request):
    """
    Executes a pipeline that populates the database with Github metadata that has been gathered using the Github REST API.
    """
    creator = GithubObjectCreator()
    creator.create_github_metadata()

    return HttpResponse('Done')

def clean(request):
    repo_count = GithubRepo.objects.count()
    account_count = GithubAccount.objects.count()

    GithubRepoLanguage.objects.filter(language_contribution=0).delete()
    GithubRepo.objects.annotate(language_count=Count("programming_languages")).filter(language_count=0).delete()
    # GithubRepo.objects.filter(pushed_at__lt=timezone.now() - timedelta(days=(365 * 3) + 14)).delete()
    GithubAccount.objects.annotate(repo_count=Count("repos")).filter(repo_count=0).delete()

    GithubAccountLanguage.objects.filter(language_share=0).delete()
    GithubAccount.objects.annotate(language_count=Count("programming_languages")).filter(language_count=0).delete()

    # GithubAccount.objects.annotate(all_contributions=Sum('contributions__contributions_count')).filter(all_contributions=0).delete()

    return HttpResponse(f'Deleted GithubAccount objects: {account_count - GithubAccount.objects.count()}, Deleted GithubRepo objects: {repo_count - GithubRepo.objects.count()}')
    

class GithubAccountView(APIView):
    def get(self, request, candidate_id):
        github_account = GithubAccount.objects.get(owner__id=candidate_id)
        serializer = FullGithubAccountSerializer(github_account, many=False)

        return Response(serializer.data)

class GithubAccountDatasetView(APIView):
    permission_classes = [IsAdminUser]

    if os.getenv('PRODUCTION') and os.getenv('USE_CLOUD_SQL_AUTH_PROXY') and (os.getenv('PRODUCTION') == 'FALSE' or os.getenv('USE_CLOUD_SQL_AUTH_PROXY') == 'TRUE'):
        permission_classes = [AllowAny]

    def get(self, request):
        accounts = GithubAccount.objects.all()
        serializer = RawGithubAccountSerializer(accounts, many=True)

        return Response(serializer.data)

# class GithubAccountDumpView(APIView):
#     permission_classes = [IsAdminUser]

#     if os.getenv('PRODUCTION') and os.getenv('USE_CLOUD_SQL_AUTH_PROXY') and (os.getenv('PRODUCTION') == 'FALSE' or os.getenv('USE_CLOUD_SQL_AUTH_PROXY') == 'TRUE'):
#         permission_classes = [AllowAny]

#     def get(self, request):
#         accounts = GithubAccount.objects.all()
        
#         data = [{
#             'id': account.user_id,
#             'login': account.username,
#             'name': account.name,
#             'bio': None,
#             'location': account.location,
#             'email': account.email,
#             'blog': account.website,
#             'company': account.company,
#             'hireable': account.hireable,
#             'html_url': account.profile_html_url,
#             'created_at': account.account_created_at,
#             'followers': account.followers_count,
#             'following': account.following_count,
#         } for account in accounts]

#         return Response(data)
