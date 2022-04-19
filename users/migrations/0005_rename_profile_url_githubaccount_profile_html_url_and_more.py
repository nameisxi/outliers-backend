# Generated by Django 4.0.3 on 2022-04-17 02:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repos', '0002_rename_repo_url_githubrepo_repo_html_url_and_more'),
        ('users', '0004_rename_repo_count_githubaccount_repos_count_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='githubaccount',
            old_name='profile_url',
            new_name='profile_html_url',
        ),
        migrations.RemoveField(
            model_name='githubaccount',
            name='repos_url',
        ),
        migrations.AddField(
            model_name='githubaccount',
            name='gists_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='githubaccount',
            name='profile_api_url',
            field=models.CharField(default='tmp', max_length=255),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='GithubContributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.githubaccount')),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repos.githubrepo')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]