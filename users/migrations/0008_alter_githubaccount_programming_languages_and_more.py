# Generated by Django 4.0.3 on 2022-04-17 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_githubaccount_programming_languages_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githubaccount',
            name='programming_languages',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='githubaccount',
            name='technologies',
            field=models.TextField(null=True),
        ),
    ]