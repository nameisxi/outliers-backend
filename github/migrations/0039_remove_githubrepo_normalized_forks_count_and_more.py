# Generated by Django 4.0.4 on 2022-06-08 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0038_rename_normalized_followers_following_counts_difference_githubaccount_normalized_follower_following_'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='githubrepo',
            name='normalized_forks_count',
        ),
        migrations.RemoveField(
            model_name='githubrepo',
            name='normalized_programming_languages_count',
        ),
        migrations.RemoveField(
            model_name='githubrepo',
            name='normalized_size_in_bytes',
        ),
        migrations.RemoveField(
            model_name='githubrepo',
            name='normalized_stargazers_count',
        ),
        migrations.RemoveField(
            model_name='githubrepo',
            name='normalized_watchers_count',
        ),
        migrations.RemoveField(
            model_name='githubrepo',
            name='programming_languages_count',
        ),
        migrations.RemoveField(
            model_name='githubrepo',
            name='repo_api_url',
        ),
    ]
