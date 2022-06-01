from django.contrib import admin

from .models import *


class OpeningAdmin(admin.ModelAdmin):
    list_display = ('get_company', 'title', 'status', 'years_of_experience_min', 'years_of_experience_max', 'created_at', 'updated_at', )

    @admin.display()
    def get_company(self, obj):
        return obj.company.name


admin.site.register(Opening, OpeningAdmin)
