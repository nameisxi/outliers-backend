# Generated by Django 4.0.4 on 2022-05-30 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openings', '0015_opening_opening_updated_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opening',
            name='years_of_experience_max',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
    ]
