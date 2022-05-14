from django.urls import path

from . import views

urlpatterns = [
    path('create-opening/', views.CreateOpeningView.as_view()),
]
