# Generated by Django 4.0.3 on 2022-04-17 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_delete_githubcontributor'),
    ]

    operations = [
        migrations.AddField(
            model_name='githubaccount',
            name='programming_languages',
            field=models.TextField(default="['TODO']"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='githubaccount',
            name='technologies',
            field=models.TextField(default="['TODO']"),
            preserve_default=False,
        ),
    ]
