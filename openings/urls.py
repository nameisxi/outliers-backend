from django.urls import path

from . import views

urlpatterns = [
    path('', views.OpeningList.as_view()),
    path('create-opening/', views.CreateOpeningView.as_view()),
]
