from django.urls import path

from . import views

urlpatterns = [
    path('compute/', views.compute),
    path('distributions/', views.get_distributions),
]
