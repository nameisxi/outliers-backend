from django.contrib import admin

from .models import *


class GithubAccountLanguageInline(admin.TabularInline):
    model = GithubAccountLanguage
    

admin.site.register(GithubAccount)
admin.site.register(GithubAccountLanguage)
admin.site.register(GithubAccountTechnology)
admin.site.register(GithubAccountTopic)

admin.site.register(GithubRepo)
admin.site.register(GithubRepoLanguage)
admin.site.register(GithubRepoTechnology)
admin.site.register(GithubRepoTopic)
