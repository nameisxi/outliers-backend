from django.urls import path

from . import views

urlpatterns = [
    path('scrape/', views.scrape),
    path('scrape/accounts/', views.scrape_accounts),
    path('scrape/organizations/', views.scrape_organizations),
    path('scrape/contributions/', views.scrape_contributions),
    path('scrape/repos/', views.scrape_repos),
    path('scrape/languages/', views.scrape_languages),
    path('populate/', views.populate),
    path('populate/accounts/', views.populate_accounts),
    path('populate/metadata/', views.populate_metadata),
    path('<int:candidate_id>/', views.GithubAccountView.as_view()),
    path('datasets/accounts/', views.GithubAccountDatasetView.as_view()),
    path('clean/', views.clean),
    # path('dumps/accounts/', views.GithubAccountDumpView.as_view()),
]
