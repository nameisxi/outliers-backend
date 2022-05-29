# Generated by Django 4.0.4 on 2022-05-29 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0022_githubaccountlanguage_language_share_current_year_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GithubOrganization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('organization_id', models.BigIntegerField()),
                ('name', models.CharField(max_length=255)),
                ('avatar_url', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]