from django.urls import path

from . import views

urlpatterns = [
    path('unique-values/', views.get_unique_values),
]
