from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import *


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'last_login')

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'created_at', 'updated_at')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Candidate)
admin.site.register(CandidateProfile)
admin.site.register(CandidatePreProfile)

admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyDomainName)

admin.site.register(Employee, EmployeeAdmin)