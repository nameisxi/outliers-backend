from django.db import models

from .base_model import BaseModel
from users.models import Candidate
from users.models import Company


class Opening(BaseModel):
    opening_candidate = models.ForeignKey('OpeningCandidate', on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)


class OpeningCandidate(BaseModel):
    # TODO do we need a join table in the first place?
    # TODO: which on_delete option to choose
    opening = models.ForeignKey('Opening', on_delete=models.PROTECT)
    candidate = models.ForeignKey(Candidate, on_delete=models.PROTECT)
