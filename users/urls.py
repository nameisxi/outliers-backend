from django.urls import path

from . import views

urlpatterns = [
    path('candidates/', views.CandidateList.as_view()),
    path('initialize/', views.initialize),
]
