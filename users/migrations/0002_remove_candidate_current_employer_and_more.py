# Generated by Django 4.0.4 on 2022-04-26 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidate',
            name='current_employer',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='current_title',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='email',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='github_url',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='linkedin_url',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='location',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='name',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='university',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='website_url',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='years_of_experience',
        ),
    ]
