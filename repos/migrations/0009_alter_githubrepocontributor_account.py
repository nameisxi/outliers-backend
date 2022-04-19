# Generated by Django 4.0.3 on 2022-04-19 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_remove_githubaccount_programming_languages_and_more'),
        ('repos', '0008_githubrepo_size_in_kilobytes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githubrepocontributor',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributions', to='users.githubaccount'),
        ),
    ]
