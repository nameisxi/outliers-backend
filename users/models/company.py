from django.db import models

from .base_model import BaseModel


class Company(BaseModel):
    name = models.CharField(max_length=255)


class CompanyDomainName(BaseModel):
    company = models.ForeignKey('Company', related_name='domain_names', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    