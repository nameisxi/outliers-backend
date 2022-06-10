from django.contrib import admin

from .models import *
# from github.admin import GithubAccountLanguageInline


class ProgrammingLanguageAdmin(admin.ModelAdmin):
    fields = ('name', )
    # inlines = [
    #     GithubAccountLanguageInline,
    # ]


admin.site.register(ProgrammingLanguage, ProgrammingLanguageAdmin)
admin.site.register(Technology)
admin.site.register(Topic)
