from django.urls import path

from . import views

urlpatterns = [
    path('', views.OpeningList.as_view()),
    path('<int:opening_id>/', views.OpeningList.as_view()),
    path('create/', views.CreateOpeningView.as_view()),
    path('update/<int:opening_id>/', views.UpdateOpeningView.as_view()),
]
