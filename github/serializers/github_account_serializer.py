from rest_framework import serializers

from technologies.serializers import ProgrammingLanguageSerializer, TechnologySerializer, TopicSerializer
from ..models import *


class GithubAccountLanguageSerializer(serializers.ModelSerializer):
    language = ProgrammingLanguageSerializer()

    class Meta:
        model = GithubAccountLanguage
        fields = ['language', 'language_share', 'language_share_current_year', 'language_share_second_year', 'language_share_third_year']
        depth = 1


class GithubAccountTechnologySerializer(serializers.ModelSerializer):
    technology = TechnologySerializer()

    class Meta:
        model = GithubAccountTechnology
        fields = ['technology']
        depth = 1


class GithubAccountTopicSerializer(serializers.ModelSerializer):
    topic = TopicSerializer()

    class Meta:
        model = GithubAccountTopic
        fields = ['topic', 'topic_share']
        depth = 1


class GithubAccountSerializer(serializers.ModelSerializer):
    programming_languages = GithubAccountLanguageSerializer(many=True, read_only=True)
    technologies = GithubAccountTechnologySerializer(many=True, read_only=True)
    topics = GithubAccountTopicSerializer(many=True, read_only=True)

    class Meta:
        model = GithubAccount
        fields = ['id', 'programming_languages', 'technologies', 'topics']
        depth = 1
