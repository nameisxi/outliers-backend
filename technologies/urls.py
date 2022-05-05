from django.urls import path

from . import views

urlpatterns = [
    path('values/', views.get_unique_values),
]
