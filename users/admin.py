from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import *


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'last_login')


class CompanyDomainNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_company', 'created_at', 'updated_at')

    @admin.display()
    def get_company(self, obj):
        return obj.company.name

class CompanyDomainNameInline(admin.TabularInline):
    model = CompanyDomainName


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    fields = ('name', )
    inlines = [
        CompanyDomainNameInline,
    ]


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_company', 'created_at', 'updated_at', 'last_visit')

    @admin.display()
    def get_company(self, obj):
        return obj.company.name


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Candidate)
admin.site.register(CandidateProfile)
admin.site.register(CandidatePreProfile)

admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyDomainName, CompanyDomainNameAdmin)

admin.site.register(Employee, EmployeeAdmin)