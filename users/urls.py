from django.urls import path
from rest_framework.authtoken import views as token_views

from . import views

urlpatterns = [
    path('employee/signup/', views.EmployeeSignupView.as_view()),
    # path('candidate/signup/', views.CandidateSignupView),
    path('login/', views.UserLoginView.as_view()),
    path('token/', token_views.obtain_auth_token),
    path('initialize/', views.initialize),
    path('candidates/', views.CandidateList.as_view()),
    
]
