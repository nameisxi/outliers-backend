# Generated by Django 4.0.4 on 2022-05-18 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('openings', '0007_openinglocation'),
    ]

    operations = [
        migrations.AddField(
            model_name='opening',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='openings.openinglocation'),
        ),
    ]
