# Generated by Django 4.0.4 on 2022-05-23 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0019_githubrepo_pushed_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='githubaccount',
            name='github_account_created_at',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='githubrepo',
            name='repo_created_at',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='githubrepo',
            name='repo_updated_at',
            field=models.DateField(null=True),
        ),
    ]
