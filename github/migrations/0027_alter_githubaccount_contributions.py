# Generated by Django 4.0.4 on 2022-05-29 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0026_githubaccount_contributions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githubaccount',
            name='contributions',
            field=models.ManyToManyField(related_name='account', to='github.githubcontributionscalendar'),
        ),
    ]
