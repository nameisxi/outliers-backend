# Generated by Django 4.0.4 on 2022-05-29 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0027_alter_githubaccount_contributions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githubcontributionscalendar',
            name='daily_max',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='githubcontributionscalendar',
            name='daily_median',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='githubcontributionscalendar',
            name='daily_min',
            field=models.IntegerField(null=True),
        ),
    ]
