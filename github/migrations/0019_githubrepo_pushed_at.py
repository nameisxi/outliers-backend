# Generated by Django 4.0.4 on 2022-05-23 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0018_delete_githubrepocontributor'),
    ]

    operations = [
        migrations.AddField(
            model_name='githubrepo',
            name='pushed_at',
            field=models.DateTimeField(null=True),
        ),
    ]