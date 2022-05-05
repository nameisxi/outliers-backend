from django.urls import path

from . import views

urlpatterns = [
    path('calculate-scores/', views.calculate_scores),
    path('distributions/', views.get_distributions),
]
