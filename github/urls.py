from django.urls import path

from . import views

urlpatterns = [
    path('create-accounts/', views.create_github_accounts),
    path('create-repos/', views.create_github_repos),
    path('add-programming-languages/', views.add_programming_languages),
    path('add-programming-languages-counts/', views.add_programming_languages_counts),
    path('get-common-repos/', views.get_repos_with_common_contributors),
    path('get-contact-details/', views.get_contact_details),
]
