# Generated by Django 4.0.3 on 2022-04-17 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_githubaccount_programming_languages_json_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='githubaccount',
            name='programming_languages',
        ),
        migrations.RemoveField(
            model_name='githubaccount',
            name='technologies',
        ),
    ]
