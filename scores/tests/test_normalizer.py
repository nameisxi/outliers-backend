from django.test import TestCase

from users.models import Candidate
from github.models import GithubAccount, GithubRepo
from ..src import Normalizer


class TestNormalizer(TestCase):
    objects_and_fields = {
        GithubAccount: [
            'repos_count',
            'gists_count',
            'contributions_count',
            'followers_count',
            'followers_following_counts_difference',
        ],
        GithubRepo: [
            'size_in_kilobytes',
            'programming_languages_count',
            'stargazers_count',
            'forks_count',
            'watchers_count',
        ],
    }

    def test_constructor(self):
        normalizer = Normalizer()

        assert(normalizer._random_state == 42)

    def test_normalize_fields(self):
        normalizer = Normalizer()
        normalizer.normalize_fields(self.objects_and_fields)

        for object_class, fields in self.objects_and_fields.items():
            for object in object_class.objects.all():
                for field in fields:
                    assert(round(getattr(object, f'normalized_{field}'), 3) >= -1.0)
                    assert(round(getattr(object, f'normalized_{field}'), 3) <= 1.0)

    def test_scale_distribution(self):
        pass

