from django.contrib import admin

from .models import *

admin.site.register(GithubRepo)
admin.site.register(GithubRepoContributor)
