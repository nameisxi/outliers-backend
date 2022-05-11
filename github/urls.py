from django.urls import path

from . import views

urlpatterns = [
    path('scrape/', views.populate),
    path('populate/', views.populate),
]
