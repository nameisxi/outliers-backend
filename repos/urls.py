from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('create-repos/', views.create_repos),
    path('common-repos/', views.get_repos_with_common_contributors),
]
