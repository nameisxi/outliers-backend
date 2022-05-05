from django.urls import path

from . import views

urlpatterns = [
    path('filter-values/', views.get_unique_technologies),
]
