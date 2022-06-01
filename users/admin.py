from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import *


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'last_login')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Candidate)
admin.site.register(CandidateProfile)
admin.site.register(CandidatePreProfile)
admin.site.register(Company)
admin.site.register(CompanyDomainName)
admin.site.register(Employee)