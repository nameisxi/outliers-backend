# Generated by Django 4.0.4 on 2022-05-14 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openings', '0002_rename_base_compensation_opening_base_compensation_min_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opening',
            name='base_compensation_max',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='opening',
            name='equity_compensation_max',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='opening',
            name='equity_compensation_min',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='opening',
            name='other_compensation_max',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='opening',
            name='other_compensation_min',
            field=models.IntegerField(null=True),
        ),
    ]