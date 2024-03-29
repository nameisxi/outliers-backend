# Generated by Django 4.0.4 on 2022-05-20 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_companydomainname'),
        ('openings', '0011_alter_opening_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpeningCandidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('saved', models.BooleanField(default=False)),
                ('stage', models.CharField(choices=[('Lead', 'Lead')], max_length=255)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.candidate')),
                ('opened_by', models.ManyToManyField(to='users.employee')),
                ('opening', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidates', to='openings.opening')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
