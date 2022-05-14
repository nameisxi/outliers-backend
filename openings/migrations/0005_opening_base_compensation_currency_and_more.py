# Generated by Django 4.0.4 on 2022-05-14 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openings', '0004_remove_opening_years_of_experience_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='opening',
            name='base_compensation_currency',
            field=models.CharField(choices=[('usd', 'USD'), ('eur', 'EUR'), ('krw', 'KRW')], default='usd', max_length=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='opening',
            name='equity_compensation_currency',
            field=models.CharField(choices=[('usd', 'USD'), ('eur', 'EUR'), ('krw', 'KRW')], default='usd', max_length=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='opening',
            name='other_compensation_currency',
            field=models.CharField(choices=[('usd', 'USD'), ('eur', 'EUR'), ('krw', 'KRW')], default='usd', max_length=3),
            preserve_default=False,
        ),
    ]
