from django.urls import path

from . import views

urlpatterns = [
    path('calculate-scores/', views.calculate_scores),
    path('distributions/', views.get_distributions),
    path('<str:github_username>/', views.get_score),
]
