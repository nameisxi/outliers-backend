# Generated by Django 4.0.4 on 2022-05-10 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0014_githubaccounttechnology_technology_share'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githubrepocontributor',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributionsjoin', to='github.githubaccount'),
        ),
    ]
