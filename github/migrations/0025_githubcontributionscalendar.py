# Generated by Django 4.0.4 on 2022-05-29 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0024_githubaccount_organizations'),
    ]

    operations = [
        migrations.CreateModel(
            name='GithubContributionsCalendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('year', models.IntegerField()),
                ('daily_min', models.IntegerField()),
                ('daily_max', models.IntegerField()),
                ('daily_median', models.IntegerField()),
                ('contributions_count', models.BigIntegerField()),
                ('contributions', models.JSONField()),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
