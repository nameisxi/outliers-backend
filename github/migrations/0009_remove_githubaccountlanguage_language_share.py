# Generated by Django 4.0.4 on 2022-05-03 04:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0008_githubaccountlanguage_language_share'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='githubaccountlanguage',
            name='language_share',
        ),
    ]
