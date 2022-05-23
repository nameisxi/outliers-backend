from django.urls import path

from . import views

urlpatterns = [
    path('scrape/', views.scrape),
    path('populate/', views.populate),
    path('<int:candidate_id>/', views.GithubAccountView.as_view()),
]
