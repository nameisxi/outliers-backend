# Generated by Django 4.0.4 on 2022-05-10 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0017_rename_repositories_githubaccount_repos'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GithubRepoContributor',
        ),
    ]
