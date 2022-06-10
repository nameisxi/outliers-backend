from rest_framework import serializers

from ..models import *


class RawGithubAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = GithubAccount
        fields = [
            'user_id',
            'contributions_count',
            'repos_count',
            'codebase_size',
            'language_count',
            'topic_count',
            'stargazer_count',
            'average_stargazer_count',
            'fork_count',
            'average_fork_count',
            'watcher_count',
            'average_watcher_count',
            'average_codebase_size',
            'average_language_count',
            'follower_following_count_difference',
        ]
