# Generated by Django 4.0.4 on 2022-05-29 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0025_githubcontributionscalendar'),
    ]

    operations = [
        migrations.AddField(
            model_name='githubaccount',
            name='contributions',
            field=models.ManyToManyField(to='github.githubcontributionscalendar'),
        ),
    ]
