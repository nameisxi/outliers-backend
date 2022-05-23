# Generated by Django 4.0.4 on 2022-05-20 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openings', '0010_alter_opening_years_of_experience_min'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opening',
            name='status',
            field=models.CharField(choices=[('Sourcing', 'Sourcing'), ('Interviewing', 'Interviewing'), ('Offering', 'Offering'), ('Hiring', 'Hiring'), ('Closed', 'Closed')], max_length=255),
        ),
    ]