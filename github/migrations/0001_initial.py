# Generated by Django 4.0.4 on 2022-04-25 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('technologies', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GithubAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_id', models.IntegerField()),
                ('username', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255, null=True)),
                ('location', models.CharField(max_length=255, null=True)),
                ('email', models.CharField(max_length=255, null=True)),
                ('website', models.CharField(max_length=255, null=True)),
                ('company', models.CharField(max_length=255, null=True)),
                ('hireable', models.BooleanField(null=True)),
                ('repos_count', models.IntegerField()),
                ('normalized_repos_count', models.FloatField()),
                ('gists_count', models.IntegerField()),
                ('normalized_gists_count', models.FloatField()),
                ('contributions_count', models.IntegerField()),
                ('normalized_contributions_count', models.FloatField()),
                ('followers_count', models.IntegerField()),
                ('normalized_followers_count', models.FloatField()),
                ('followers_following_counts_difference', models.IntegerField()),
                ('normalized_followers_following_counts_difference', models.FloatField()),
                ('profile_html_url', models.CharField(max_length=255)),
                ('profile_api_url', models.CharField(max_length=255)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='github_accounts', to='users.candidate')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GithubRepo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('repo_id', models.BigIntegerField()),
                ('name', models.CharField(max_length=255)),
                ('stargazers_count', models.IntegerField()),
                ('normalized_stargazers_count', models.FloatField()),
                ('forks_count', models.IntegerField()),
                ('normalized_forks_count', models.FloatField()),
                ('watchers_count', models.IntegerField()),
                ('normalized_watchers_count', models.FloatField()),
                ('size_in_kilobytes', models.BigIntegerField()),
                ('normalized_size_in_kilobytes', models.FloatField()),
                ('repo_html_url', models.CharField(max_length=255)),
                ('repo_api_url', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GithubRepoTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='github.githubrepo')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='technologies.topic')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GithubRepoTechnology',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='technologies', to='github.githubrepo')),
                ('technology', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='technologies.technology')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GithubRepoLanguage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('language_share', models.FloatField()),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='technologies.programminglanguage')),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='programming_languages', to='github.githubrepo')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GithubRepoContributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributions', to='github.githubaccount')),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='github.githubrepo')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
