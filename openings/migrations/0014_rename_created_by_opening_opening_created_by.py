# Generated by Django 4.0.4 on 2022-05-30 04:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('openings', '0013_alter_opening_created_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='opening',
            old_name='created_by',
            new_name='opening_created_by',
        ),
    ]
