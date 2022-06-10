import json

from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from github.models import GithubAccount, GithubAccountLanguage, GithubAccountTopic
from technologies.models import ProgrammingLanguage, Topic
from ..models import *
from ..views import CandidateList


class CandidateListTestCase(APITestCase):
    user = User.objects.create(
        username='testuser',
        email='testuser@test.com'
    )
    user.set_password('test1234')
    user.save()

    fields = {
            'work_score': -1,
            'popularity_score': -1,
            'hireability_score': -1,
            'fit_score': -1,
    }
    candidate1 = Candidate(**fields)
    candidate1.save()
    candidate2 = Candidate(**fields)
    candidate2.save()
    candidate3 = Candidate(**fields)
    candidate3.save()

    fields = {
        'account_created_at': '2022-06-08',
        'user_id': -1,
        'username': 'test',
        'name': 'test',
        'location': 'test',
        'email': 'test',
        'website': 'test',
        'company': 'test',
        'hireable': True,
        'followers_count': 1,
        'following_count': 2,
        'profile_html_url':'http://www.github.com/test',
    }
    gh_account1 = GithubAccount(**fields)
    gh_account1.owner = candidate1
    gh_account1.save()
    gh_account2 = GithubAccount(**fields)
    gh_account2.owner = candidate2
    gh_account2.save()
    gh_account3 = GithubAccount(**fields)
    gh_account3.owner = candidate3
    gh_account3.save()

    language1 = ProgrammingLanguage(name='python')
    language1.save()
    language2 = ProgrammingLanguage(name='java')
    language2.save()
    language3 = ProgrammingLanguage(name='go')
    language3.save()
    gh_account_language1 = GithubAccountLanguage(
                                account=gh_account1, 
                                language=language1,
                                language_share=0.2,
                                language_share_current_year=-1.0,
                                language_share_second_year=-1.0,
                                language_share_third_year=-1.0,
                            )
    gh_account_language1.save()
    gh_account_language2 = GithubAccountLanguage(
                                account=gh_account1, 
                                language=language2,
                                language_share=0.1,
                                language_share_current_year=-1.0,
                                language_share_second_year=-1.0,
                                language_share_third_year=-1.0,
                            )
    gh_account_language2.save()
    gh_account_language3 = GithubAccountLanguage(
                                account=gh_account2, 
                                language=language2,
                                language_share=0.1,
                                language_share_current_year=-1.0,
                                language_share_second_year=-1.0,
                                language_share_third_year=-1.0,
                            )
    gh_account_language3.save()
    gh_account_language4 = GithubAccountLanguage(
                                account=gh_account2, 
                                language=language3,
                                language_share=0.01,
                                language_share_current_year=-1.0,
                                language_share_second_year=-1.0,
                                language_share_third_year=-1.0,
                            )
    gh_account_language4.save()
    gh_account_language5 = GithubAccountLanguage(
                                account=gh_account3, 
                                language=language1,
                                language_share=0.01,
                                language_share_current_year=-1.0,
                                language_share_second_year=-1.0,
                                language_share_third_year=-1.0,
                            )
    gh_account_language5.save()
    gh_account_language6 = GithubAccountLanguage(
                                account=gh_account3, 
                                language=language3,
                                language_share=0.7,
                                language_share_current_year=-1.0,
                                language_share_second_year=-1.0,
                                language_share_third_year=-1.0,
                            )
    gh_account_language6.save()

    topic1 = Topic(name='nlp')
    topic1.save()
    topic2 = Topic(name='crypto')
    topic2.save()
    topic3 = Topic(name='android')
    topic3.save()
    gh_account_topic1 = GithubAccountTopic(
                                account=gh_account1, 
                                topic=topic1,
                                topic_share=0.2
                            )
    gh_account_topic1.save()
    gh_account_topic2 = GithubAccountTopic(
                                account=gh_account1, 
                                topic=topic2,
                                topic_share=0.1
                            )
    gh_account_topic2.save()
    gh_account_topic3 = GithubAccountTopic(
                                account=gh_account2, 
                                topic=topic2,
                                topic_share=0.1
                            )
    gh_account_topic3.save()
    gh_account_topic4 = GithubAccountTopic(
                                account=gh_account2, 
                                topic=topic3,
                                topic_share=0.01
                            )
    gh_account_topic4.save()
    gh_account_topic5 = GithubAccountTopic(
                                account=gh_account3, 
                                topic=topic1,
                                topic_share=0.01
                            )
    gh_account_topic5.save()
    gh_account_topic6 = GithubAccountTopic(
                                account=gh_account3, 
                                topic=topic3,
                                topic_share=0.7
                            )
    gh_account_topic6.save()

    def test_result_size_without_filters(self):
        factory = APIRequestFactory()
        view = CandidateList.as_view()

        request = factory.get('/candidates/?format=json')
        force_authenticate(request, user=self.user)
        response = view(request)

        assert(len(response.data) == Candidate.objects.all().count())

    def test_result_size_with_limit_filter(self):
        factory = APIRequestFactory()
        view = CandidateList.as_view()

        request = factory.get('/candidates/?format=json&limit=2')
        force_authenticate(request, user=self.user)
        response = view(request)
        response.render()
        response = json.loads(response.content)

        request2 = factory.get('/candidates/?format=json&limit=1')
        force_authenticate(request2, user=self.user)
        response2 = view(request2)
        response2.render()
        response2 = json.loads(response2.content)
        
        assert(len(response['results']) == 2)
        assert(len(response2['results']) == 1)

    def test_result_size_with_one_programming_language_filter(self):
        factory = APIRequestFactory()
        view = CandidateList.as_view()

        request = factory.get('/candidates/?format=json&language=python')
        force_authenticate(request, user=self.user)
        response = view(request)
        response.render()
        response = json.loads(response.content)

        request2 = factory.get('/candidates/?format=json&language=java')
        force_authenticate(request2, user=self.user)
        response2 = view(request2)
        response2.render()
        response2 = json.loads(response2.content)

        request3 = factory.get('/candidates/?format=json&language=go')
        force_authenticate(request3, user=self.user)
        response3 = view(request3)
        response3.render()
        response3 = json.loads(response3.content)

        assert(len(response) == 1)
        assert(len(response2) == 2)
        assert(len(response3) == 1)

    def test_result_size_with_two_programming_language_filters(self):
        factory = APIRequestFactory()
        view = CandidateList.as_view()

        request = factory.get('/candidates/?format=json&language=python&language=java')
        force_authenticate(request, user=self.user)
        response = view(request)
        response.render()
        response = json.loads(response.content)

        request2 = factory.get('/candidates/?format=json&language=java&language=go')
        force_authenticate(request2, user=self.user)
        response2 = view(request2)
        response2.render()
        response2 = json.loads(response2.content)

        request3 = factory.get('/candidates/?format=json&language=go&language=python')
        force_authenticate(request3, user=self.user)
        response3 = view(request3)
        response3.render()
        response3 = json.loads(response3.content)

        assert(len(response) == 1)
        assert(len(response2) == 0)
        assert(len(response3) == 0)

    def test_result_size_with_one_topic_filter(self):
        factory = APIRequestFactory()
        view = CandidateList.as_view()

        request = factory.get('/candidates/?format=json&topic=nlp')
        force_authenticate(request, user=self.user)
        response = view(request)
        response.render()
        response = json.loads(response.content)

        request2 = factory.get('/candidates/?format=json&topic=crypto')
        force_authenticate(request2, user=self.user)
        response2 = view(request2)
        response2.render()
        response2 = json.loads(response2.content)

        request3 = factory.get('/candidates/?format=json&topic=android')
        force_authenticate(request3, user=self.user)
        response3 = view(request3)
        response3.render()
        response3 = json.loads(response3.content)

        assert(len(response) == 1)
        assert(len(response2) == 2)
        assert(len(response3) == 1)

    def test_result_size_with_two_topic_filters(self):
        factory = APIRequestFactory()
        view = CandidateList.as_view()

        request = factory.get('/candidates/?format=json&topic=nlp&topic=crypto')
        force_authenticate(request, user=self.user)
        response = view(request)
        response.render()
        response = json.loads(response.content)

        request2 = factory.get('/candidates/?format=json&topic=crypto&topic=android')
        force_authenticate(request2, user=self.user)
        response2 = view(request2)
        response2.render()
        response2 = json.loads(response2.content)

        request3 = factory.get('/candidates/?format=json&topic=android&topic=nlp')
        force_authenticate(request3, user=self.user)
        response3 = view(request3)
        response3.render()
        response3 = json.loads(response3.content)

        assert(len(response) == 1)
        assert(len(response2) == 0)
        assert(len(response3) == 0)

    def test_result_size_mixed_filters(self):
        factory = APIRequestFactory()
        view = CandidateList.as_view()

        request = factory.get('/candidates/?format=json&language=java')
        force_authenticate(request, user=self.user)
        response = view(request)
        response.render()
        response = json.loads(response.content)

        request2 = factory.get('/candidates/?format=json&topic=crypto')
        force_authenticate(request2, user=self.user)
        response2 = view(request2)
        response2.render()
        response2 = json.loads(response2.content)

        request3 = factory.get('/candidates/?format=json&language=java&topic=crypto')
        force_authenticate(request3, user=self.user)
        response3 = view(request3)
        response3.render()
        response3 = json.loads(response3.content)

        request4 = factory.get('/candidates/?format=json&language=java&topic=nlp')
        force_authenticate(request4, user=self.user)
        response4 = view(request4)
        response4.render()
        response4 = json.loads(response4.content)

        assert(len(response) == 2)
        assert(len(response2) == 2)
        assert(len(response3) == 2)
        assert(len(response4) == 1)
