# Generated by Django 4.0.4 on 2022-05-04 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0011_githubaccounttopic_topics_share'),
    ]

    operations = [
        migrations.RenameField(
            model_name='githubaccounttopic',
            old_name='topics_share',
            new_name='topic_share',
        ),
    ]