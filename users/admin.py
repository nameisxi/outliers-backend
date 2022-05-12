from django.contrib import admin

from .models import *


admin.site.register(Candidate)
admin.site.register(CandidateProfile)
admin.site.register(CandidatePreProfile)
admin.site.register(Company)
admin.site.register(CompanyDomainName)
admin.site.register(Employee)