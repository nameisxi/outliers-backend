# Generated by Django 4.0.4 on 2022-06-08 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0042_githubaccount_account_scraped_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='githubaccount',
            old_name='github_account_created_at',
            new_name='account_created_at',
        ),
    ]
