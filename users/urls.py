from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.CandidateList.as_view()),
    path('create-candidates/', views.create_candidates),
]
